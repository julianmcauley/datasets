import sys
import json
import pylab as plt
from collections import Counter

def load_json(fn):
  with open(fn) as f:
    data = json.load(f)

  game_list = []
  user_list = []
  data_dict = {}
  for d in data:
    for gida in d['game_id']:
      gid = int(gida)
      game_list.append(gid)
      uid = int(d['user_id'])
      user_list.append(uid)

      if not uid in data_dict:
        data_dict[uid] = []
      data_dict[uid].append(gid)

  return data_dict, game_list, user_list

def getBinningOfVector(measuredVariable):
	frequencyBins = dict()
	for value in measuredVariable:
		if value in frequencyBins:
			frequencyBins[value] += 1
		else:
			frequencyBins[value] = 1

	variable = []
	frequency = []
	for variableValue, freq in frequencyBins.items():
		variable.append(variableValue)
		frequency.append(freq)

	return [variable, frequency]

def nbOfTimeInList(data, dict_list):
  data = set(data)

  len_list = []
  for d in data:
    cnt = 0
    for k,v in dict_list.iteritems():
      if d in v:
        cnt += 1
    len_list.append(cnt)

  return len_list

def getListsSize(dict_list):
  list_len = []
  for k,v in dict_list.iteritems():
    list_len.append(len(v))
  return list_len

if __name__ == "__main__":
  have_file = "../scripts/dataset/itemlist.json"
  wish_file = "../scripts/dataset/wishlist.json"

  # Load a dict of data
  # Key is the user_id
  have_dict, have_game, have_user = load_json(have_file)
  wish_dict, wish_game, wish_user = load_json(wish_file)

  print "Wish data points[tot/game/user]:", len(wish_game), len(set(wish_game)), len(set(wish_user))
  print "Have data points[tot/game/user]:", len(have_game), len(set(have_game)), len(set(have_user))

  fig = plt.figure()
  [havePopularity, frequency] = getBinningOfVector(nbOfTimeInList(have_game, have_dict))
  plt.scatter(havePopularity, frequency, s=30, linewidths=0, c=(0.9290, 0.6940, 0.1250), alpha=0.8)
  plt.yscale('log', nonposy='clip')
  plt.xscale('log', nonposy='clip')
  plt.ylim([1.0, 10 ** 2])
  plt.xlim([1.0, 10 ** 3])
  plt.xlabel('Number of different give-away lists that a game appears in \n ("have" popularity)', fontsize=16)
  plt.ylabel('Number of games', fontsize=16)
  plt.grid(True)
  plt.savefig('giveAwayItemPopularity.pdf', bbox_inches='tight')
  plt.show()

  fig = plt.figure()
  [havePopularity, frequency] = getBinningOfVector(nbOfTimeInList(wish_game, wish_dict))
  plt.scatter(havePopularity, frequency, s=30, linewidths=0, c=(0.9290, 0.6940, 0.1250), alpha=0.8)
  plt.yscale('log', nonposy='clip')
  plt.xscale('log', nonposy='clip')
  plt.ylim([1.0, 10 ** 2])
  plt.xlim([1.0, 10 ** 3])
  plt.xlabel('Number of different wish lists that a game appears in \n ("wish" popularity)', fontsize=16)
  plt.ylabel('Number of games', fontsize=16)
  plt.grid(True)
  plt.savefig('haveItemPopularity.pdf', bbox_inches='tight')
  plt.show()

  fig = plt.figure()
  [itemListLengths, frequency] = getBinningOfVector(getListsSize(have_dict))
  plt.scatter(itemListLengths, frequency,  s=30, linewidths=0, c=(0.0, 0.4470, 0.7410), alpha=0.8)
  plt.yscale('log', nonposy='clip')
  plt.xscale('log', nonposy='clip')
  plt.ylim([1.0, 10**3])
  plt.xlim([1.0, 10**3])
  plt.xlabel('Give-away list size (number of games)', fontsize=16)
  plt.ylabel('Number of users', fontsize=16)
  plt.grid(True)
  plt.savefig('giveAwayListLength.pdf', bbox_inches='tight')
  plt.show()

  fig = plt.figure()
  [wishListLengths, frequency] = getBinningOfVector(getListsSize(wish_dict))
  plt.scatter(wishListLengths, frequency,  s=30, linewidths=0, c=(0.0, 0.4470, 0.7410), alpha=0.8)
  plt.yscale('log', nonposy='clip')
  plt.xscale('log', nonposy='clip')
  plt.ylim([1.0, 10 ** 3])
  plt.xlim([1.0, 10 ** 3])
  plt.xlabel('Wish list size (number of games)', fontsize=16)
  plt.ylabel('Number of users', fontsize=16)
  plt.grid(True)
  plt.savefig('wishListLength.pdf', bbox_inches='tight')
  plt.show()



