from utils_swapi import *

# This scripts load the final dataset and check its consistency with the data gathered with the web crawler

# Dictionaries
user_userid = dict()
userid_user = dict()

game_gameid = dict()
gameid_game = dict()

wishlist = list()
itemlist = list()
query_gameid = dict()
control = dict()


# Here we load the final dataset into different dictionaries to later check consistency
# Create dictionaries user->user_id and user_id->user from final dataset
with open("files/user_userid.json") as data_file:
    print "Load users"
    data = json.load(data_file)
    for d in data:
        user_userid[d['username']] = d['id']
        userid_user[d['id']] = d['username']

# Create dictionaries game->game_id and game_id->game from final dataset
with open("files/game_gameid.json") as data_file:
    print "Load games"
    data = json.load(data_file)
    for d in data:
        game_gameid[d['game']] = d['id']
        gameid_game[d['id']] = d['game']

# Create dictionary query->game_id from final dataset
with open("files/query_gameid.json") as data_file:
    print "Load queries"
    data = json.load(data_file)
    for d in data:
        query_gameid[d['query']] = d['id']

# Load wish list
with open("files/wishlist.json") as data_file:
    print "Load wishlist"
    data = json.load(data_file)
    for d in data:
        wishlist.append([d['user_id'], d['game_id']])

# Load item list
with open("files/itemlist.json") as data_file:
    print "Load itemlist"
    data = json.load(data_file)
    for d in data:
        itemlist.append([d['user_id'], d['game_id']])

print "user_id:", len(user_userid)
print "game_id:", len(game_gameid)
print "Number of items in itemlist:", len(itemlist)
print "Number of items in wishlists:", len(wishlist)


# Check success trade threads
nbr_swap = 0
nbr_games = 0
with open('files/success.json') as f:
    data = json.load(f)
    for i, d in enumerate(data):
        # Get authors name
        a1 = userid_user[d['user1']]
        a2 = userid_user[d['user2']]
        # Get list of games id
        g1 = d['game1']
        g2 = d['game2']
        l1 = []
        l2 = []
        nbr_swap += 1

        # Get game names from games ids
        for i in g1:
            nbr_games += 1
            l1.append(gameid_game[i])
        for i in g2:
            nbr_games += 1
            l2.append(gameid_game[i])

        #print "%s: %s\n%s: %s\n" % (a1, l1, a2, l2)
print "Nbr of swap:", nbr_swap
print "Nbr of games:", nbr_games


# Build dictionary from itemlist and wishlist
for item in itemlist:
    user = userid_user[item[0]]
    games = []
    for g in item[1]:
        games.append(g)
    if user in control:
        wish = control[user][0]
        item = control[user][1]
        for x in games:
            item.append(x)
        control[user] = [wish, item]
    else:
        wish = []
        item = []
        for x in games:
            item.append(x)
        control[user] = [wish, item]

for item in wishlist:
    user = userid_user[item[0]]
    games = []
    for g in item[1]:
        games.append(g)
    if user in control:
        wish = control[user][0]
        item = control[user][1]
        for x in games:
            wish.append(x)
        control[user] = [wish, item]
    else:
        wish = []
        item = []
        for x in games:
            wish.append(x)
        control[user] = [wish, item]


with open('data/submissions.json') as f:
    data = json.load(f)
    for i, d in enumerate(data):
        current_wishlist = set()
        current_itemlist = set()

        # Process games from body
        body_games, ok = process_body(d, console_tags)

        if ok:
            wants = body_games['wants']
            haves = body_games['haves']
            for entry in wants:
                if entry['tag_matched']:
                    current_wishlist.add(remove_specials_char(entry['name']))
            for entry in haves:
                if entry['tag_matched']:
                    current_itemlist.add(remove_specials_char(entry['name']))

        # Process game from title
        title = d['title']
        if len(title) != 0:
            gamesByTag = getTags(title)
            if 'h' in gamesByTag:
                have = gamesByTag['h']
                have = [x.strip().encode('utf-8') for x in have.split(',')]
                addInSet(current_itemlist, have)

            if 'w' in gamesByTag:
                want = gamesByTag['w']
                want = [x.strip().encode('utf-8') for x in want.split(',')]
                addInSet(current_wishlist, want)

        if len(current_itemlist) + len(current_wishlist) == 0:
            continue

        user = d['author'].lower()

        for w in current_wishlist:
            if w in query_gameid:
                game_id = query_gameid[w]
                assert game_id in control[user][0]
        for itm in current_itemlist:
            if itm in query_gameid:
                game_id = query_gameid[itm]
                assert game_id in control[user][1]

print "Dictionary length:", len(control)
print "Tests finished"
