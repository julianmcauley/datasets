import sys
import json
from roman import *
from BeautifulSoup import BeautifulSoup
import BeautifulSoup as bs


# Return the levenshtein distance between a and b
def levenshtein(a, b):
    a = a.lower()
    b = b.lower()
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current = range(n+1)
    for i in range(1, m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1, n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current[j] = min(add, delete, change)

    return current[n]


# Return the query, game and levenshtein distance between the query and the closest match in the list of
# answer returned by giantbomb
def shortest_levenshtein(query, gb_ans):
    keywords = ['for', 'or', 'any', 'offers', 'offer', 'link', 'confirmed', 'and', 'proof', 'swap', '\'s']
    dist = sys.maxint
    game = ""
    original_query = query
    query = remove_specials_char(query.lower())
    # Check all answer returned by giantBomb
    for ans in gb_ans:
        current_query = query
        ans = ans[1]
        # Compute distance
        current_dist = levenshtein(current_query, ans)
        # If distance is better, save game and corresponding distance
        if current_dist < dist:
            dist = current_dist
            game = ans
        # If there is an exact match, we can already return the answer
        if dist == 0:
            return [original_query, game, dist]

        # The following code are the rules to try to reduce the Levenshtein distance and match more games
        # For more information, look in the report (section "Validating game names")

        # Try removing punctuation from giantbomb
        gb_game = re.sub(r'[^\w\s]', "", ans)
        current_dist = levenshtein(current_query, gb_game)
        if current_dist < dist:
            dist = current_dist
            game = ans
            ans = gb_game

        if dist == 0:
            return [original_query, game, dist]

        # Try removing useless info to reduce distance
        for r in console_tags:
            q = current_query.replace(r, "")
            q = remove_specials_char(q)
            current_dist = levenshtein(q, ans)
            if current_dist < dist:
                dist = current_dist
                current_query = q
        if dist == 0:
            return [original_query, game, dist]

        for w in keywords:
            q = current_query.replace(w, "")
            q = remove_specials_char(q)
            current_dist = levenshtein(q, ans)
            if current_dist < dist:
                dist = current_dist
                current_query = q
        if dist == 0:
            return [original_query, game, dist]

        # Try replacing acronyms
        for acro in dict_key:
            low = current_query.lower()
            if low.find(acro) != -1:
                q = current_query.replace(acro, acronyms[acro])
                q = remove_specials_char(q)
                current_dist = levenshtein(q, ans)
                if current_dist < dist:
                    dist = current_dist
                    current_query = q
        if dist == 0:
            return [original_query, game, dist]

        # Try transforming numbers to roman numbers
        nbr_in_query = re.findall(r'[0-9]+', current_query)
        for nbr in nbr_in_query:
            try:
                q = current_query.replace(nbr, toRoman(int(nbr)))
            except:
                continue
            current_dist = levenshtein(q, ans)
            if current_dist < dist:
                dist = current_dist
                current_query = q

        if dist == 0:
            return [original_query, game, dist]

        # Try removing isolated char
        isolated_char = re.findall(r'\b[\w]\b', current_query)
        for c in isolated_char:
            regexp = r'\b[%s]\b' % (c)
            q = re.sub(regexp, "", query)
            q = remove_specials_char(q)
            current_dist = levenshtein(q, ans)
            if current_dist < dist:
                dist = current_dist
                current_query = q

        if dist == 0:
            return [original_query, game, dist]

        new_gb = ans.replace("the", "")
        current_dist = levenshtein(current_query, new_gb)
        if current_dist < dist:
            dist = current_dist
            game = ans

        if dist == 0:
            return [original_query, game, dist]

    return [original_query, game, dist]


# Try removing special characters at beginning or end of extracted game names
def remove_specials_char(string):
    string = re.sub(r"^\W+", "", string)
    string = re.sub(r"\W+$", "", string)
    string = string.replace("  ", " ")
    return string


# Add all element from list in the set
def addInSet(set, list):
    for element in list:
        if len(element) != 0:
            set.add(remove_specials_char(element))


# Return tags
def getTags(title):
    tag_have = ['h', 'have']
    tag_want = ['w', 'want']
    title = title.lower()
    tags = dict()
    for t in tag_have:
        regex = '.*[\[(]' + t + '[\])]([^\[]*)'
        m = re.findall(regex, title)
        if len(m) != 0:
            str = re.sub('\s*\(.*\)\s*', '', m[0])
            tags['h'] = str.strip()
            break

    for t in tag_want:
        regex = '.*[\[(]' + t + '[\])]([^\[]*)'
        m = re.findall(regex, title)
        if len(m) != 0:
            str = re.sub('\s*\(.*\)\s*', '', m[0])
            tags['w'] = str.strip()
            break
    return tags


# The console tags are stored in a file. Load them in a list
def get_console_tags():
    # Read console tags
    with open('data/console_tags.txt', 'r') as f:
        console_tags = f.readlines()
        console_tags = [line.rstrip('\n') for line in console_tags]
    return console_tags


# A dictionary of gaming related acronyms(from http://www.abbreviations.com/acronyms/GAMING) is stored in acronyms.json.
# Load it in dictionary
def get_acronyms():
    # Read acronyms from json file
    acronyms = dict()
    with open('data/acronyms.json', 'r') as data_file:
        data = json.load(data_file)
        for d in data:
            acronyms[d['short'].lower()] = d['full']
    return acronyms


# Return both trading partners and list of games exchanged for successful swaps
def get_trade_info(trade):
    trade = trade.replace("\n", "")
    # get both trading partners
    [author1, author2] = re.findall(r'\(([^\)]*)\)', trade)
    author1 = author1.lower()
    author2 = author2.lower()
    assert author1 != "" and author2 != ""
    # get trades body
    txt = re.sub(r'\(([^\)]*)\)', "", trade)
    # removing multiple whitespace
    txt = re.sub(' +', ' ', txt)
    # Separate games belonging to author1 and author2
    splitted = txt.split(" for ")
    assert len(splitted) == 2
    game_u1 = []
    game_u2 = []

    game_u1 = re.split(",", splitted[0])
    game_u2 = re.split(",", splitted[1])
    game_u1 = [remove_specials_char(x) for x in game_u1]
    game_u2 = [remove_specials_char(x) for x in game_u2]

    return [author1, game_u1, author2, game_u2]


# All the following functions were implemented by Jeremie Rappaz
def get_tag_from_previous(table):
    pot_p = table.findAllPrevious('p')
    if len(pot_p) > 0:
        pot_p = pot_p[0]
        return pot_p.getText()
    else:
        return ""


def match_tag_from_lst(txt, lst):
    txt = txt.lower()
    for l in lst:
        if l.lower() in txt:
            return True, l
    return False, txt


# Remove element in list lst from the string str
def rem_from_str(txt, lst):
    for l in lst:
        txt = txt.replace(l, "")
    return txt


def post_process_el(element):
    element, lst = list_and_rem_parent(element)

    # Remove what's after those token plus the token itself
    element = rem_after_char(element, ["-", ",", "w/"])

    # Remove blindly
    element = rem_from_str(element, ["=", "*", "/"])

    # Remove the token as a word (only if it has space after or before)
    element, tok = rem_token_from_str(element, ['NA', 'OOB', 'CI',
                                                'CIB', 'NIB', 'IB',
                                                "CART", "EU", "loose",
                                                "sealed", "JP", "US",
                                                "USA", "CAN"])

    element = rem_numbers(element)

    # Remove encoding problems
    element = replace_char(element)

    element = element.strip()
    element = element.encode('utf-8')
    return (element, tok)


def rem_after_char(sent, lst):
    for l in lst:
        sent = sent.split(l, 1)[0]
    return sent


def rem_numbers(txt):
    txt_l = txt.split(" ")
    pattern = re.compile('\d')
    if pattern.search(txt_l[0]) is not None:
        txt = txt.replace(txt_l[0], "")
        txt = txt.strip()
    return txt


def replace_char(txt):
    txt = txt.replace('&#39;', "'")
    txt = txt.replace('&amp;', '&')
    return txt


def discard_if_contains(txt, lst):
    if len(txt) < 3:
        return False
    for l in lst:
        if l.lower() in txt.lower():
            return False
    return True


def rem_token_from_str(txt, lst):
    tokens = []

    for l in lst:
        if str(" " + l.lower()) in txt.lower():
            pattern = re.compile(l, re.IGNORECASE)
            txt = pattern.sub("", txt)
            tokens.append(l.lower())
        elif str(l.lower() + " ") in txt.lower():
            pattern = re.compile(l, re.IGNORECASE)
            txt = pattern.sub("", txt)
            tokens.append(l.lower())

    return (txt, tokens)


# Remove the parenthesis from string
def rem_parent(l):
    l = l.replace("(", "")
    l = l.replace(")", "")
    l = l.replace("[", "")
    l = l.replace("]", "")
    return l


# Remove items in parenthesis and return them as a list of tags
def list_and_rem_parent(sent):
    sent = sent.replace('&#39;', "'")

    lst = re.findall('\(.*?\)',sent)
    lst += re.findall('\[.*?\]',sent)

    lst_split = []
    for l in lst:
        if "," in l:
            tlst = re.split(',|;|\/|&|\+',l)
            for tl in tlst:
                tl = re.sub(r'\([^)]*\)', '', tl)
                tl = rem_parent(tl)
                lst_split.append(tl.strip())
        else:
            lst_split.append(rem_parent(l))

    sent = re.sub(r"[\(\[].*?[\)\]]", '', sent)

    add = []
    for l in lst_split:
        ls = re.split(',|;|\/|&|\+',l)
        add += ls

    add = list(set(add))
    return (sent, add)


# Process the body of a post
def process_body(d, console_tags):
    body = d['body_html']

    DISCARD_LIST = ['more', 'list', 'any', 'offer', 'please']

    soup = BeautifulSoup(body)

    tables = soup.findAll('tr')
    lists = soup.findAll('ul')
    ps = soup.findAll('p')

    ele = soup.find('div', {'class': 'md'})

    children = ele.findChildren() if ele is not None else []

    # This defines the current list mode
    # Default is "have"
    mode = 'h'

    # No structure
    # --> no chocolate
    if len(tables) == 0 or len(lists) == 0:
        return {}, False

    json_post = {}
    json_post['author'] = d['author']
    json_post['id'] = d['id']
    json_post['wants'] = []
    json_post['haves'] = []

    for e in ele:
        if isinstance(e, bs.Tag):
            element = ""
            tok = ""

            if e.name == 'p':

                token_w = ['want', 'lookingfor']
                token_h = ['have', 'fortrade', 'got']

                txt = e.getText().lower()
                txt = rem_from_str(txt, [',', '/', ':', '.', '!', '-', ' '])

                for t in token_w:
                    if t in txt:
                        if 'youwant' not in t:
                            mode = 'w'

                for t in token_h:
                    if t in txt:
                        mode = 'h'

            if e.name == 'table':
                act_tag = get_tag_from_previous(e)
                act_tag = rem_from_str(act_tag, [',', '/', ':', '.', '!', '-'])
                ok, act_tag = match_tag_from_lst(act_tag, console_tags)

                head = e.find('thead')

                # Try to guess the right column of the table
                idx = -1
                ths = head.findAll('th')
                for i in xrange(len(ths)):
                    head_title = ths[i].getText().lower()
                    head_pos = ['title', 'game', 'accessor', 'book', 'hardware']
                    for p in head_pos:
                        if p in head_title:
                            idx = i
                            break

                if idx is not -1:
                    body = e.find('tbody')
                    trs = body.findAll('tr')

                    el_list = []
                    for t in trs:
                        tds = t.findAll('td')

                        try:
                            element = tds[idx].getText()
                        except IndexError:
                            continue

                        element, tok = post_process_el(element)

                        if discard_if_contains(element, DISCARD_LIST):
                            eljs = {}
                            eljs['name'] = element
                            eljs['tag'] = act_tag
                            eljs['tag_matched'] = ok
                            eljs['token'] = tok
                            el_list.append(eljs)

                    # Correct the mode
                    if 'want' in act_tag.lower():
                        mode = 'w'
                    elif 'have' in act_tag.lower():
                        mode = 'h'

                    if mode == 'h':
                        json_post['wants'] += el_list
                    elif mode == 'w':
                        json_post['haves'] += el_list

                else:
                    #print bcolors.WARNING + "Failed reading table" + bcolors.ENDC
                    pass

            if e.name == 'ul':
                act_tag = get_tag_from_previous(e)
                act_tag = rem_from_str(act_tag, [',', '/', ':', '.', '!', '-'])
                ok, act_tag = match_tag_from_lst(act_tag, console_tags)

                li = e.findAll('li')
                el_list = []
                for l in li:
                    element = l.getText()
                    element, tok = post_process_el(element)

                    if discard_if_contains(element, DISCARD_LIST):
                        eljs = {}
                        eljs['name'] = element
                        eljs['tag'] = act_tag
                        eljs['tag_matched'] = ok
                        eljs['token'] = tok
                        el_list.append(eljs)

                # Correct the mode
                if 'want' in act_tag.lower():
                    mode = 'w'
                elif 'have' in act_tag.lower():
                    mode = 'h'

                if mode == 'h':
                    json_post['wants'] += el_list
                elif mode == 'w':
                    json_post['haves'] += el_list

    return json_post, True


console_tags = get_console_tags()
acronyms = get_acronyms()
dict_key = acronyms.keys()
