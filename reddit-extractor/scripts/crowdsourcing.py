import os
import re
import json
# This script sort the posts in the success thread and write
# the potentially useful ones in a text file


# Make body more readable: remove links and line return
def process_body(body):
    # removing links
    body = re.sub(r'https?://(\S+)', '', body)
    # remove new line
    body = body.replace("\n", " ")
    return body


# Write string to text file
def write_to_file(string):
    with open("data/success_swap_unsorted.txt", "a") as myfile:
        myfile.write(string.encode('utf-8'))


confirm = 0
no_confirm = 0
tot = 0
replies = 0
for file in os.listdir("./data/success_threads"):
    with open('data/success_threads/' + file) as data_file:
        if file == ".DS_Store":
            continue
        print "analyse of: ", file
        data = json.load(data_file)

        # user 1, game 1, user 2, game 2
        success_swap = list()
        # keys = [u'body', u'author', u'id', (u'replies')]
        json_tot = []
        c = 0
        for d in data:
            body = d['body'].lower()
            # If those keywords are found in the body, users don't swap games, but one user buy a game from the other.
            # This information is useless for us, so we discard it
            if '$' in body or 'paypal' in body or 'sale' in body or 'sold' in body or 'bought' in body or 'purchase' in body:
                continue

            # Get username of swapping partners
            author1 = d['author']
            tot += 1
            # if no replies: drop post
            if 'replies' not in d.keys():
                no_confirm += 1
                continue
            replies += 1
            # Parse comment to find confirmation from second user
            author2 = None
            for com in d['replies']:
                low = com['body'].lower()
                if "confirm" in low or "success" in low or "true" in low or "confirmed" in low or "thank" in low \
                    or "comfirmed" in low or "good" in low or "enjoy" in low:
                    author2 = com['author']
                    break
            # If second user does not confirm, drop post
            if author2 is None:
                continue

            # Write exchange in txt file in following format: (author1) body (author2)
            string = "(%s) %s (%s)\n" % (author1, process_body(body), author2)
            write_to_file(string)
            confirm += 1

print "tot:", tot, "confirm:", confirm, "no:", no_confirm,  "reply:", replies
