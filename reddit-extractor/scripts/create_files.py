# -*- coding: utf-8 -*-
import os
from utils_swapi import *

# Solve encoding problems in game names
reload(sys)
sys.setdefaultencoding('utf-8')

# levenshtein threshold
levenshtein_trsh = 1
users_userid = dict()
query_gameid = dict()


# Write string to text file
def write_to_txt_file(file_name, string):
    with open(file_name, "a") as myfile:
        myfile.write(string.encode('utf-8'))


# Create dictionary with game->game_id
def create_query_gameid():
    game_gameid = dict()
    game_idx = 0
    # Process all files in the "QueryGiantBomb" folder
    for file in os.listdir("./data/QueryGiantBomb"):
        with open('data/QueryGiantBomb/' + file) as data_file:
            if file == ".DS_Store":
                continue
            print "Process", file
            data = json.load(data_file)
            for d in data:
                query = d['query']
                gb_ans = d['giantbomb']
                # Get the game with shortest levenshtein distance
                [q, a, current_dist] = shortest_levenshtein(query, gb_ans)
                if current_dist <= levenshtein_trsh:
                    print query, "->", a
                    # If the game already exists, pick its id
                    if a in game_gameid:
                        id = game_gameid[a]
                    # Else take new unique id for game
                    else:
                        game_gameid[a] = game_idx
                        id = game_idx
                        game_idx += 1
                    query_gameid[query] = id

    print "Number of games:", len(game_gameid)
    print "Number of query->games:", len(query_gameid)

    # Create json and text files
    # Create game_gameid.txt and game_gameid.json
    json_tot = []
    for game, gameid in game_gameid.iteritems():
        json_entry = {}
        json_entry['game'] = game
        json_entry['id'] = gameid
        json_tot.append(json_entry)
        s = "%s -> %d\n" % (game, gameid)
        write_to_txt_file('dataset/game_gameid.txt', s)
    file_name = "dataset/game_gameid.json"
    with open(file_name, 'w') as f:
        json.dump(json_tot, f)

    # Create query_gameid.txt and query_gameid.json
    json_tot = []
    for query, gameid in query_gameid.iteritems():
        json_entry = {}
        json_entry['query'] = query
        json_entry['id'] = gameid
        json_tot.append(json_entry)
        s = "%s -> %d\n" % (query, gameid)
        write_to_txt_file('dataset/query_gameid.txt', s)
    file_name = "dataset/query_gameid.json"
    with open(file_name, 'w') as f:
        json.dump(json_tot, f)


# Create dictionary with user->user_id
def create_user_userid():
    users = set()
    with open('data/submissions.json') as f:
        data = json.load(f)

        # Get all users from swap thread
        for i, d in enumerate(data):
            users.add(d['author'].lower())
        print "Number of users (swap thread):", len(users)
    # Get all users from success thread
    with open('data/success_swap.txt') as f:
        for trade in f:
            [author1, game_u1, author2, game_u2] = get_trade_info(trade)
            users.add(author1.lower())
            users.add(author2.lower())
        print "Number of users (success + swap thread):", len(users)

    # Create files user_userid.txt and user_userid.json
    json_tot = []
    user_id = 0
    for u in users:
        u = u.lower()
        users_userid[u] = user_id
        json_user = {}
        json_user['id'] = user_id
        json_user['username'] = u
        json_tot.append(json_user)
        s = "%d -> %s\n" % (user_id, u)
        write_to_txt_file('dataset/user_userid.txt', s)
        user_id += 1


    file_name = "dataset/user_userid.json"
    with open(file_name, 'w') as f:
        json.dump(json_tot, f)


# Recursive function that search the games in the list "games" in the comments
def search_comments(comments, games, dic_wish):
    body = comments['body'].lower()
    author = comments['author'].lower()
    # Search game names in comments:
    for g in games:
        # If a game appear in the comment
        if g in body:
            # Fetch author's set of games
            if author not in dic_wish:
                dic_wish[author] = set()
            l = dic_wish[author]
            # Add game in set
            l.add(g)
            # To debug, write game and body in text file
            s = "(((%s))) %s" %(g, body)
            write_to_txt_file("test_com.txt", s)
    if "replies" in comments:
        for reply in comments['replies']:
            search_comments(reply, games, dic_wish)


# Create wishlist and itemlist
def create_wishlist_itemlist():
    augmented_wish_size = 0
    itemlist = dict()
    wishlist = dict()
    p = 0
    # Open file (Posts extracted from Gameswap with crawler)
    with open('data/submissions.json') as f:
        data = json.load(f)
        for i, d in enumerate(data):
            # Wishlist and itemlist for the current post
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

            # Get author of post
            user = d['author'].lower()
            # Get author's id
            user_id = users_userid[user]
            # Get author wishlist
            if user_id not in wishlist:
                wishlist[user_id] = set()
            list_of_wishes = wishlist[user_id]
            # Get author itemlist
            if user_id not in itemlist:
                itemlist[user_id] = set()
            list_of_item = itemlist[user_id]

            # Add current wish to existing wishlist
            for game in current_wishlist:
                if game in query_gameid:
                    game_id = query_gameid[game]
                    list_of_wishes.add(game_id)

            # Game name to look for in the comments (implicit feedback)
            clean_item_list = set()
            # Add current items to existing itemlist
            for game in current_itemlist:
                if game in query_gameid:
                    game_id = query_gameid[game]
                    list_of_item.add(game_id)
                    clean_item_list.add(game)

            # Process comments: If a user is interested in a game, add it to its wishlist
            augmented_wishlist = dict()
            # If a post has comments
            if 'comments' in d and len(clean_item_list) > 0:
                # Look for implicit feedback in comments
                for com in d['comments']:
                    search_comments(com, clean_item_list, augmented_wishlist)
            augmented_wish_size += len(augmented_wishlist)
            # If we found implicit feedback, add game in user's wishlist
            if len(augmented_wishlist) > 0:
                for user, games in augmented_wishlist.iteritems():
                    if user in users_userid:
                        com_user_id = users_userid[user]
                        # To prevent adding game in it's owner wishlist
                        if com_user_id != user_id and len(games) > 0:
                            # Get current list for user
                            if com_user_id not in wishlist:
                                wishlist[com_user_id] = set()
                            list_of_wishes = wishlist[com_user_id]
                            # Add games in wishlist
                            for g in games:
                                game_id = query_gameid[g]
                                list_of_wishes.add(game_id)
            # Print something in console every 1000 posts processed
            if i-p >= 1000:
                print i
                p = i

        print "Augmented wishlist:", augmented_wish_size
        # Create JSON files
        json_tot = []
        for user_id, game_id in wishlist.iteritems():
            if len(game_id) > 0:
                json_entry = {}
                json_entry['user_id'] = user_id
                json_entry['game_id'] = list(game_id)
                json_tot.append(json_entry)
        file_name = "dataset/wishlist.json"
        with open(file_name, 'w') as f:
            json.dump(json_tot, f)

        json_tot = []
        for user_id, game_id in itemlist.iteritems():
            if len(game_id) > 0:
                json_entry = {}
                json_entry['user_id'] = user_id
                json_entry['game_id'] = list(game_id)
                json_tot.append(json_entry)
        file_name = "dataset/itemlist.json"
        with open(file_name, 'w') as f:
            json.dump(json_tot, f)


# Create JSON with successful swap
def create_success_trade():
    json_swaps = []
    cancel = 0
    # Open file that was manually sorted
    with open('data/success_swap.txt') as f:
        # For each success swap
        for trade in f:
            # Get trading partners and games exchanged
            [author1, game_u1, author2, game_u2] = get_trade_info(trade)
            # Store game id
            gb_u1 = []
            gb_u2 = []
            # Get game ids (user 1)
            for game in game_u1:
                if game in query_gameid:
                    game_id = query_gameid[game]
                    gb_u1.append(game_id)
            # Get game ids (user 2)
            for game in game_u2:
                if game in query_gameid:
                    game_id = query_gameid[game]
                    gb_u2.append(game_id)
            # If one of list is empty, i.e we only have one side of the trade, drop
            if len(gb_u1) == 0 or len(gb_u2) == 0:
                cancel += 1
                continue
            # Get authors id
            author1_id = users_userid[author1]
            author2_id = users_userid[author2]

            # Save successful swap
            json_trade = {}
            json_trade['user1'] = author1_id
            json_trade['game1'] = gb_u1
            json_trade['user2'] = author2_id
            json_trade['game2'] = gb_u2
            json_swaps.append(json_trade)

    # Write all successful swap to JSON file
    print "Number of trades:", len(json_swaps)
    print "cancelled:", cancel
    file_name = "dataset/success.json"
    with open(file_name, 'w') as f:
        json.dump(json_swaps, f)


# During testing, instead of generating user_userid.json and query_gameid.json
# every time, load them from file.
def load_files():
    with open("dataset/user_userid.json") as data_file:
        print "Load users"
        data = json.load(data_file)
        for d in data:
            users_userid[d['username'].lower()] = d['id']

    with open("dataset/query_gameid.json") as data_file:
        print "Load queries"
        data = json.load(data_file)
        for d in data:
            query_gameid[d['query']] = d['id']


create_user_userid()
create_query_gameid()
create_success_trade()
create_wishlist_itemlist()
