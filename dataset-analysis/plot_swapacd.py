#!/usr/bin/env python3

__author__ = 'Dih0r'

import json
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

#---------------------------------------------------------------------------------------------------------------------
#-----------------------------------GET DATA INTO ARRAYS FOR HISTOGRAMMING--------------------------------------------
#---------------------------------------------------------------------------------------------------------------------

def get_list_size_vectors(userData, itemlistSize, wishlistSize):

	for user in userData:
		itemlistSize.append(len(user["itemlist"]))
		wishlistSize.append(len(user["wishlist"]))

def get_cdf_frequency_vectors(cdData, number_of_times_in_itemlist, number_of_times_in_wishlist):

	for cd in cdData:
		number_of_times_in_itemlist.append(int(cdData[cd]["numberOfAppearancesInItemlist"]))
		number_of_times_in_wishlist.append(int(cdData[cd]["numberOfAppearancesInWishlist"]))


def create_input_file_for_plots(input_path):

	itemlist_size = []
	wishlist_size = []
	number_of_times_in_itemlist = []
	number_of_times_in_wishlist = []

	with open(input_path + 'users.json') as users:
			user_data = json.load(users)

	with open(input_path + 'cds.json') as cds:
			cd_data = json.load(cds)


	get_list_size_vectors(user_data, itemlist_size, wishlist_size)
	get_cdf_frequency_vectors(cd_data, itemlist_size, wishlist_size)

	target = open(input_path + "statisticsCD.txt", 'w')
	target.write(itemlist_size.__str__())
	target.write("\n")
	target.write(wishlist_size.__str__())
	target.write("\n")
	target.write(number_of_times_in_itemlist.__str__())
	target.write("\n")
	target.write(number_of_times_in_wishlist.__str__())
	target.write("\n")

	print("Wrote statisticsCD.txt")

	return user_data


def get_binning_of_values(measured_variable):
	frequency_bins = dict()
	for value in measured_variable:
		if value in frequency_bins:
			frequency_bins[value] += 1
		else:
			frequency_bins[value] = 1

	variable = []
	frequency = []
	for var_value, freq in frequency_bins.items():
		variable.append(var_value)
		frequency.append(freq)

	return [variable, frequency]

def get_data(input_path):

	with open(input_path + "statisticsCD.txt") as f:
		content = f.readlines()

	itemlistSize = list(map(int, content[0].replace("[", "").replace("]", "").split(",")))
	wishlistSize = list(map(int, content[1].replace("[", "").replace("]", "").split(",")))
	numberOfTimesInItemlist = list(map(int, content[2].replace("[", "").replace("]", "").split(",")))
	numberOfTimesInWishlist = list(map(int, content[3].replace("[", "").replace("]", "").split(",")))

	return [itemlistSize, wishlistSize, numberOfTimesInItemlist, numberOfTimesInWishlist]


def plot_give_away_list_size_distribution(plot_path, itemlist_size):
	out_filename = 'giveAwayListLength.pdf'
	plt.close('all')

	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	[giveaway_list_lengths, frequency] = get_binning_of_values(itemlist_size)
	plt.scatter(giveaway_list_lengths, frequency,  s=30, linewidths=0, c=(0.0, 0.4470, 0.7410), alpha=0.8)
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.ylim([1.0, 10**3])
	plt.xlim([1.0, 10**5])
	plt.xlabel('Give-away list size (number of CDs) \n (log scale)', fontsize=16)
	plt.ylabel('Number of users \n(log scale)', fontsize=16)
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote plot " + out_filename)


def plot_wish_list_size_distribution(plot_path, wishlist_size):
	out_filename = 'wishListLength.pdf'
	plt.close('all')

	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	[wishlist_lengths, frequency] = get_binning_of_values(wishlist_size)
	plt.scatter(wishlist_lengths, frequency,  s=30, linewidths=0, c=(0.0, 0.4470, 0.7410), alpha=0.8)
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.ylim([1.0, 10 ** 3])
	plt.xlim([1.0, 10 ** 5])
	plt.xlabel('Wish list size (number of CDs) \n (log scale)', fontsize=16)
	plt.ylabel('Number of users \n(log scale)', fontsize=16)
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote plot " + out_filename)


def plot_item_have_popularity(plot_path, number_of_times_in_itemlist):
	out_filename = 'giveAwayItemPopularity.pdf'
	plt.close('all')

	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	[have_popularity, frequency] = get_binning_of_values(number_of_times_in_itemlist)
	plt.scatter(have_popularity, frequency, s=30, linewidths=0, c=(0.9290, 0.6940, 0.1250), alpha=0.8)
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.ylim([1.0, 10 ** 6])
	plt.xlim([1.0, 10 ** 3])
	plt.xlabel('Number of different give-away lists that a CD appears in \n ("have" popularity)  \n (log scale)', fontsize=16)
	plt.ylabel('Number of CDs \n(log scale)', fontsize=16)
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote plot " + out_filename)

def plot_item_wish_popularity(plot_path, number_of_times_in_wishlist):
	out_filename = 'wishItemPopularity.pdf'
	plt.close('all')

	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	[wish_popularity, frequency] = get_binning_of_values(number_of_times_in_wishlist)
	plt.scatter(wish_popularity, frequency, s=30, linewidths=0, c=(0.9290, 0.6940, 0.1250), alpha=0.8)
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.ylim([1.0, 10 ** 6])
	plt.xlim([1.0, 10 ** 3])
	plt.xlabel('Number of different wish lists that a CD appears in \n ("wish" popularity) \n (log scale)', fontsize=16)
	plt.ylabel('Number of CDs \n(log scale)', fontsize=16)
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote plot " + out_filename)


def get_top_active_users(out_path, user_data):

	user_data.sort(key=lambda x: len(x["itemlist"]), reverse=True)
	top_ten_biggest_itemlist_users = user_data[0:10]

	user_data.sort(key=lambda x: len(x["wishlist"]), reverse=True)
	top_ten_biggest_wishlist_users = user_data[0:10]

	print("Opening the files...")

	with open(out_path + "topTenItemlist.json", 'w') as outfile:
			json.dump(top_ten_biggest_itemlist_users, outfile)

	with open(out_path + "topTenWishlist.json", 'w') as outfile:
			json.dump(top_ten_biggest_wishlist_users, outfile)

	print("Done writing top users.")


if __name__ == '__main__':
	input_path = "data_files/swapacd/"
	[itemlist_size, wishlist_size, number_of_times_in_itemlist, number_of_times_in_wishlist] = get_data(input_path)

	plots_path = 'output/swapacd/'
	plot_give_away_list_size_distribution(plots_path, itemlist_size)
	plot_wish_list_size_distribution(plots_path, wishlist_size)
	plot_item_have_popularity(plots_path, number_of_times_in_itemlist)
	plot_item_wish_popularity(plots_path, number_of_times_in_wishlist)