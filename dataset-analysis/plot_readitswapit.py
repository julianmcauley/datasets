#!/usr/bin/env python
__author__ = 'Dih0r'

import json
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt



def set_number_of_appearences_in_wishlist(user_data, book_data):
	bookHash = dict()

	for user in user_data:
		for wish in user["wishes"]:
			if bookHash.get(wish["title"], "none") == "none":
				bookHash[wish["title"]] = 1
			else :
				bookHash[wish["title"]] += 1

	return bookHash

def create_input_file_for_plots(input_path):
	with open(input_path + 'users.json') as users:
		user_data = json.load(users)

	with open(input_path + 'books.json') as books:
		book_data = json.load(books)


	itemlist_size = []
	wishlist_size = []

	for user in user_data:
		itemlist_size.append(int(user["registNum"]))
		wishlist_size.append(int(user["wishNum"]))

	number_of_times_in_itemlist = []
	number_of_times_in_wishlist = []
	bookHash = set_number_of_appearences_in_wishlist(user_data, book_data)

	for book in book_data:
		number_of_times_in_itemlist.append(int(book["copies"]))
		if bookHash.get(book["title"], "none") == "none":
			number_of_times_in_wishlist.append(0)
		else:
			number_of_times_in_wishlist.append(int(bookHash[book["title"]]))


	target = open(input_path + "statistics_readitswapit.txt", 'w')
	target.write(itemlist_size.__str__())
	target.write("\n")
	target.write(wishlist_size.__str__())
	target.write("\n")
	target.write(number_of_times_in_itemlist.__str__())
	target.write("\n")
	target.write(number_of_times_in_wishlist.__str__())
	target.write("\n")

	print("Wrote " + input_path + "statistics_readitswapit.txt")

	return user_data


def get_top_active_users(out_path, user_data):
	user_data.sort(key=lambda x: int(x["registNum"]), reverse=True)
	topFiveItemlist = user_data[:5]

	user_data.sort(key=lambda x: int(x["wishNum"]), reverse=True)
	topFiveWishlist = user_data[:5]

	print("Opening the files...")

	with open(out_path + "top_users_for_itemlist_size.json", 'w') as outfile:
			json.dump(topFiveItemlist, outfile)

	with open(out_path + "top_users_for_wishlist_size.json", 'w') as outfile:
			json.dump(topFiveWishlist, outfile)

	print("Wrote top users files.")

def get_binning_of_values(measuredVariable):
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

def get_data(input_path):
	with open(input_path + "statistics_readitswapit.txt") as f:
		content = f.readlines()

	itemlist_size = list(map(int, content[0].replace("[", "").replace("]", "").split(",")))
	wishlist_size = list(map(int, content[1].replace("[", "").replace("]", "").split(",")))
	number_of_times_in_itemlist = list(map(int, content[2].replace("[", "").replace("]", "").split(",")))
	number_of_times_in_wishlist = list(map(int, content[3].replace("[", "").replace("]", "").split(",")))

	return [itemlist_size, wishlist_size, number_of_times_in_itemlist, number_of_times_in_wishlist]

def plot_give_away_list_size_distribution(plot_path, itemlist_size):
	out_filename = "giveawaylist_length.pdf"
	plt.close('all')

	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	[itemlist_lengths, frequency] = get_binning_of_values(itemlist_size)
	plt.scatter(itemlist_lengths, frequency,  s=30, linewidths=0, c=(0.0, 0.4470, 0.7410), alpha=0.8)
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.xlabel('Give-away list size (number of books) \n (log scale)', fontsize=16)
	plt.ylabel('Number of users \n(log scale)', fontsize=16)
	plt.ylim([1.0, 10 ** 4])
	plt.xlim([1.0, 10 ** 4])
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote plot " + out_filename)

def plot_wish_list_size_distribution(plot_path, wishlist_size):
	out_filename = "wishlist_length.pdf"
	plt.close('all')

	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	[wishlist_lengths, frequency] = get_binning_of_values(wishlist_size)
	plt.scatter(wishlist_lengths, frequency,  s=30, linewidths=0, c=(0.0, 0.4470, 0.7410), alpha=0.8)
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.xlabel('Wish list size (number of books) \n (log scale)', fontsize=16)
	plt.ylabel('Number of users \n(log scale)', fontsize=16)
	plt.ylim([1.0, 10**4])
	plt.xlim([1.0, 10**4])
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote plot " + out_filename)

def plot_item_have_popularity(plot_path, number_of_times_in_itemlist):
	out_filename = "giveaway_item_popularity.pdf"
	plt.close('all')

	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	[have_popularity, frequency] = get_binning_of_values(number_of_times_in_itemlist)
	plt.scatter(have_popularity, frequency,  s=30, linewidths=0, c=(0.9290, 0.6940, 0.1250), alpha=0.8)
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.xlabel('Number of different give-away lists that a book appears in \n ("have" popularity) \n (log scale)', fontsize=16)
	plt.ylabel('Number of books \n(log scale)', fontsize=16)
	plt.ylim([1.0, 10**5])
	plt.xlim([1.0, 10**3])
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote plot " + out_filename)

def plot_item_wish_popularity(plot_path, number_of_times_in_wishlist):
	out_filename = "wish_item_popularity.pdf"
	plt.close('all')

	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	[wish_popularity, frequency] = get_binning_of_values(number_of_times_in_wishlist)
	plt.scatter(wish_popularity, frequency,  s=30, linewidths=0, c=(0.9290, 0.6940, 0.1250), alpha=0.8)
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.xlabel('Number of different wish lists that a book appears in \n ("wish" popularity) \n (log scale)', fontsize=16)
	plt.ylabel('Number of books \n(log scale)', fontsize=16)
	plt.ylim([1.0, 10**5])
	plt.xlim([1.0, 10**3])
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote plot " + out_filename)


if __name__ == '__main__':
	input_path = "data-files/readitswapit/"

	[itemlist_size, wishlist_size, number_of_times_in_itemlist, number_of_times_in_wishlist] = get_data(input_path)

	plots_path = "output/readitswapit/"
	plot_give_away_list_size_distribution(plots_path, itemlist_size)
	plot_wish_list_size_distribution(plots_path, wishlist_size)
	plot_item_have_popularity(plots_path, number_of_times_in_itemlist)
	plot_item_wish_popularity(plots_path, number_of_times_in_wishlist)