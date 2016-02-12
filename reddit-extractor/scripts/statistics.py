import os
from utils_swapi import *


# Counts the number of comments
def count_comments(comments):
    global nbr_comments
    nbr_comments += 1
    if "replies" in comments:
        for reply in comments['replies']:
            count_comments(reply)

# Print information on the submissions.json file
with open('data/submissions.json') as f:
    data = json.load(f)
    nbr_posts = 0
    nbr_comments = 0
    nbr_users = set()
    for i, d in enumerate(data):
        nbr_users.add(d['author'].lower())
        nbr_posts += 1
        if 'comments' in d:
            for com in d['comments']:
                count_comments(com)

print "------------- Submissions -------------"
print "Number of users:", len(nbr_users)
print "Number of posts:", nbr_posts
print "Number of comments", nbr_comments


# Print information on the success trade threads
nbr_posts = 0
nbr_money = 0
nbr_replies = 0
nbr_comments = 0
nbr_confirmed = 0
for file in os.listdir("./data/success_threads"):
    with open('data/success_threads/' + file) as data_file:
        if file == ".DS_Store":
            continue
        data = json.load(data_file)
        for i, d in enumerate(data):
            nbr_posts += 1
            body = d['body'].lower()
            if '$' in body or 'paypal' in body:
                nbr_money += 1
                continue

            if 'replies' not in d.keys():
                continue
            nbr_replies += 1

            for com in d['replies']:
                nbr_comments += 1
                low = com['body'].lower()
                if "confirm" in low or "success" in low or "true" in low:
                    nbr_confirmed += 1
print "------------- Success Thread -------------"
print "Number of posts:", nbr_posts
print "Number of swap with money:", nbr_money
print "Number of replies", nbr_replies
print "Number of comments:", nbr_comments
print "Number of confirmed:", nbr_confirmed


# Print information on the wishlist
with open('dataset/wishlist.json') as f:
    data = json.load(f)
    nbr_wishs = 0
    nbr_tot_games = 0
    nbr_games = set()
    nbr_users = set()
    for i, d in enumerate(data):
        user_id = d['user_id']
        game_id = d['game_id']
        nbr_users.add(user_id)
        nbr_tot_games += len(game_id)
        for g in game_id:
            nbr_games.add(g)
        nbr_wishs += 1

print "------------- wishlist -------------"
print "Number of users:", len(nbr_users)
print "Number of wish:", nbr_wishs
print "Number of unique games", len(nbr_games)
print "Total number of games", nbr_tot_games


# Print information on the itemlist
with open('dataset/itemlist.json') as f:
    data = json.load(f)
    nbr_items = 0
    nbr_tot_games = 0
    nbr_games = set()
    nbr_users = set()
    for i, d in enumerate(data):
        user_id = d['user_id']
        game_id = d['game_id']
        nbr_users.add(user_id)
        nbr_tot_games += len(game_id)
        for g in game_id:
            nbr_games.add(g)
        nbr_items += 1

print "------------- itemlist -------------"
print "Number of users:", len(nbr_users)
print "Number of wish:", nbr_items
print "Number of unique games", len(nbr_games)
print "Total number of games", nbr_tot_games


# Print information on the success swap
with open('dataset/success.json') as f:
    data = json.load(f)
    nbr_success = 0
    nbr_games = set()
    nbr_users = set()
    nbr_tot_games = 0
    for i, d in enumerate(data):
        user1_id = d['user1']
        game1_id = d['game1']
        user2_id = d['user2']
        game2_id = d['game2']
        nbr_users.add(user1_id)
        nbr_users.add(user2_id)
        nbr_tot_games += len(game1_id)
        nbr_tot_games += len(game2_id)
        for g in game1_id:
            nbr_games.add(g)
        for g in game2_id:
            nbr_games.add(g)

        nbr_success += 1

print "------------- success -------------"
print "Number of users:", len(nbr_users)
print "Number of success:", nbr_success
print "Number of games", len(nbr_games)
print "Total number of games", nbr_tot_games
