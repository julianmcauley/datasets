from giantbomb import giantbomb
from utils_swapi import *


def giantBomb_success_thread():
    number_of_trade = 0
    number_of_games = 0
    all_games = set()
    with open("data/success_swap.txt") as f:
        for trade in f:
            number_of_trade += 1
            [author1, game_u1, author2, game_u2] = get_trade_info(trade)
            number_of_games += len(game_u1) + len(game_u2)
            for g in game_u1:
                all_games.add(g)
            for g in game_u2:
                all_games.add(g)

    print "Set of games:", len(all_games)
    print "Number of trades:", number_of_trade
    print "Number of games:", number_of_games
    json_tot = []
    counter = 0
    for game in all_games:
        game = game.decode('utf-8')
        print counter, game
        counter += 1
        try:
            gb_response = gb.search(game)
        except:
            continue
        gb_response = gb_response[:5]
        gb_ans = []
        for i in gb_response:
            l = []
            l.append(i.id)
            l.append(i.name)
            gb_ans.append(l)
        json_gb = {}
        json_gb['query'] = game
        json_gb['giantbomb'] = gb_ans
        json_tot.append(json_gb)

    # Write to file
    file_name = "data/success_gb.json"
    with open(file_name, 'w') as f:
        json.dump(json_tot, f)


def giantBomb_posts():
    games = set()
    duplicate = 0
    size_game = 0
    with open('data/submissions.json') as f:
        data = json.load(f)

        for i, d in enumerate(data):
            # Process games from body
            body_games, ok = process_body(d, console_tags)

            if ok == True:
                wants = body_games['wants']
                haves = body_games['haves']
                for entry in wants:
                    if entry['tag_matched'] == True:
                        if entry['name'] in games:
                            duplicate += 1
                        games.add(remove_specials_char(entry['name']))
                for entry in haves:
                    if entry['tag_matched'] == True:
                        if entry['name'] in games:
                            duplicate += 1
                        games.add(remove_specials_char(entry['name']))
            # Process game from title
            title = d['title']
            if len(title) != 0:
                gamesByTag = getTags(title)
                if gamesByTag.has_key('h'):
                    have = gamesByTag['h']
                    have = [x.strip().encode('utf-8') for x in have.split(',')]
                    addInSet(games, have)
                    for element in have:
                        if len(element) != 0 and element in games:
                            duplicate += 1

                if gamesByTag.has_key('w'):
                    want = gamesByTag['w']
                    want = [x.strip().encode('utf-8') for x in want.split(',')]
                    addInSet(games, want)
                    for element in want:
                        if len(element) != 0 and element in games:
                            duplicate += 1

            if len(games)-size_game >= 200:
                size_game = len(games)
                print "Number of games processed:", size_game

    print "Number of games:", len(games)
    print "Number of duplicates:", duplicate

    json_tot = []
    game_number = 0
    file_nbr = 1
    nbr_game_per_file = 5000

    for game in games:
        game = game.decode('utf-8')
        if len(game) > 4:
            game_number += 1
            print game_number, game
            try:
                gb_response = gb.search(game)
            except:
                continue
            gb_response = gb_response[:5]
            gb_ans = []
            for i in gb_response:
                l = []
                l.append(i.id)
                l.append(i.name)
                gb_ans.append(l)
            json_gb = {}
            json_gb['query'] = game
            json_gb['giantbomb'] = gb_ans
            json_tot.append(json_gb)

        # Write to file
        if game_number % nbr_game_per_file == 0 and game_number != 0:
            file_name = "data/QueryGiantBomb/games_giantbomb_%d.json" % (file_nbr)
            file_nbr += 1
            with open(file_name, 'w') as f:
                json.dump(json_tot, f)
            json_tot = []
    file_name = "data/QueryGiantBomb/games_giantbomb_%d.json" % (file_nbr)
    with open(file_name, 'w') as f:
        json.dump(json_tot, f)

gb = giantbomb.Api('18f6f55a14bf80ae481ed72a5bad10733e46119e')
giantBomb_posts()
giantBomb_success_thread()

