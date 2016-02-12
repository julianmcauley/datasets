from elasticsearch import Elasticsearch
import os
import json
es = Elasticsearch()

# Start elastic seatch:
#   cd /usr/local/opt/elasticsearch/bin
#   ./elasticsearch

########## Elasticsearch ##########
# Here we experienced with Elasticsearch and fuzzy queries to try
# to match games name written by users and official game names


# Get all offical games names (Answers form GiantBomb)
def get_all_gb_games():
    all_giantBomb_games = set()
    for file in os.listdir("./QueryGiantBomb"):
        with open('QueryGiantBomb/' + file) as data_file:
            if file == ".DS_Store":
                continue
            print "Process", file
            data = json.load(data_file)
            for d in data:
                gb_ans = d['giantbomb']
                for game_name in gb_ans:
                    all_giantBomb_games.add(game_name[1])
    print "Number of games:", len(all_giantBomb_games)
    # Index all games name in Elastic search Node
    for g in all_giantBomb_games:
        es_index_game(g)


# Return all games indexed
def es_query_match_all():
    return es.search(index="game_idx", doc_type="game", body={"query": {"match_all": {}}})


# Try to query Elasticsearch Node
# param: game = game name
def es_query(game):
    query = json.dumps({
        "query": {
            "match": {
                "game": game
            }
        }
    })
    return es.search(index="game_idx", doc_type="game", body=query)


# Try to query Elasticsearch Node with fuzzy query
# param:    game = game name
#           fuzziness = degree of fuzziness
#           begin = beginning of sliding windows
#           size = size of sliding windows
def es_fuzzy_query(game, fuzziness, begin, size):
    query = json.dumps({
        "from": begin, "size": size,
        "query": {
            "fuzzy": {
                "game": {
                    "value": game,
                    "fuzziness": fuzziness,
                    # "boost" :         1.0,
                    "prefix_length": 0,
                    # "max_expansions": 100
                }
            }
        }
    })
    return es.search(index="game_idx", doc_type="game", body=query)


# Index game in Elasticsearch Node
# param: game = game name
def es_index_game(game):
    doc = {
        'game': game,
    }

    return es.index(index="game_idx", doc_type="game", body=doc)


# Delete game
# param: id = id of game to be deleted
def es_delete(id):
    es.delete(index="game_idx", doc_type="game", id=id)


# Display result returned by Elasticsearch
# param: res = Elasticsearch result
def es_display_res(res):
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print("%(game)s" % hit["_source"])


# Small test for fuzzy queries
def test_fuzzy():
    fuzziness = 1
    res = es_fuzzy_query("gam", fuzziness, 0, 100)

    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print("%(game)s" % hit["_source"])
