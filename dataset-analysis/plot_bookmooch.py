__author__ = 'Dih0r'
import pickle
import matplotlib as mpl
mpl.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import csv
from math import log
import math


#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------LOAD DATA---------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
def read_data_for_cdf(input_path):
	data_filled_original = pickle.load(open(input_path + "filled_original_inverted_lists.pickle", "rb"))

	return data_filled_original

def get_giver_and_receiver_frequency(input_path):

	with open(input_path + "transac.csv", "r") as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		givers = dict()
		receivers = dict()

		for line in reader:
			if line[0] in givers:
				givers[line[0]] += 1
			else:
				givers[line[0]] = 1

			if line[1] in receivers:
				receivers[line[1]] += 1
			else:
				receivers[line[1]] = 1

	givers_sorted = sorted(givers.values(), reverse = True)
	receivers_sorted = sorted(receivers.values(), reverse = True)

	return [givers_sorted, receivers_sorted]

def get_cdf_arrays_for_plot(sorted_value_vector):
	total_num_of_transactions = sum(sorted_value_vector)

	cdf_array = []
	for idx, val in enumerate(sorted_value_vector):
		if idx > 0:
			cdf_array.append(float(float(val)/float(total_num_of_transactions)) + float(cdf_array[idx - 1]))
		else:
			cdf_array.append(float(float(val)/float(total_num_of_transactions)))
	index_vector = range(1, len(sorted_value_vector) + 1)

	return [cdf_array, index_vector]

def plot_book_givers_cdf(plot_path, givers_sorted):
	out_filename = "givers_cdf.pdf"

	[percentage_of_giver_posts, index_vector] = get_cdf_arrays_for_plot(givers_sorted)

	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	plt.plot(index_vector, percentage_of_giver_posts, '-', color=(0.6350, 0.0780, 0.1840), linewidth=3)
	plt.gca().yaxis.set_ticks(np.arange(0, 1.1, 0.1))
	plt.ylim([0, 1])
	plt.xlim([0, len(index_vector) - 1])

	#========== Set tick labels to be percentages =================================
	plt.xticks(np.arange(0, len(index_vector), math.floor(len(index_vector) * 0.2)))
	labels = ['0%', '20%', '40%', '60%', '80%', '100%']
	plt.gca().set_xticklabels(labels)
	labels = ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
	plt.gca().set_yticklabels(labels)

	#==================== Plot and save ==============================
	plt.xlabel('Percentage of active givers', fontsize=16)
	plt.ylabel('Percentage of transactions covered', fontsize=16)
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

def plot_book_receivers_cdf(plot_path, receivers_sorted):
	out_filename = "receivers_cdf.pdf"

	[percentage_of_receiver_posts, index_vector] = get_cdf_arrays_for_plot(receivers_sorted)

	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	plt.plot(index_vector, percentage_of_receiver_posts, '-', color=(0.4940, 0.1840, 0.5560), linewidth=3)
	plt.gca().yaxis.set_ticks(np.arange(0, 1.1, 0.1))
	plt.ylim([0, 1])
	plt.xlim([0, len(index_vector)])

	#========== Set tick labels to be percentages =================================
	plt.xticks(np.arange(0, len(index_vector), math.floor(len(index_vector) * 0.2)))
	labels = ['0%', '20%', '40%', '60%', '80%', '100%']
	plt.gca().set_xticklabels(labels)
	labels = ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
	plt.gca().set_yticklabels(labels)

	#==================== Plot and save ==============================
	plt.xlabel('Percentage of users', fontsize=16)
	plt.ylabel('Percentage of transactions covered', fontsize=16)
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

def get_binning_of_values(measuredVariable, tolog=False):
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
		if tolog == False:
			frequency.append(freq)
		else:
			frequency.append(log(freq))

	return [variable, frequency]

def get_data(input_path):

	print("Loading a huge pickle file, be patient :D ... ")
	data_filled_original = read_data_for_cdf(input_path)

	wishlist_size = []
	for wishlist in data_filled_original[4].values():
		wishlist_size.append(len(wishlist))

	itemlist_size = []
	for itemlist in data_filled_original[3].values():
		itemlist_size.append(len(itemlist))

	number_of_times_in_itemlist = []
	for userList in data_filled_original[1].values():
		number_of_times_in_itemlist.append(len(userList))

	number_of_times_in_wishlist = []
	for userList in data_filled_original[2].values():
		number_of_times_in_wishlist.append(len(userList))

	return [wishlist_size, itemlist_size, number_of_times_in_itemlist, number_of_times_in_wishlist]

def plot_wish_list_size_distribution(plot_path, wishlist_size):
	out_filename = "wishlist_length.pdf"
	plt.close('all')
	
	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	print(len([x for x in wishlist_size if x > 100]))
	[wishlist_lengths, frequency] = get_binning_of_values(wishlist_size)
	plt.scatter(wishlist_lengths, frequency,  s=30, linewidths=0, c=(0.0, 0.4470, 0.7410), alpha=0.8)
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.ylim([1.0, 10 ** 5])
	plt.xlim([1.0, 10 ** 6])
	plt.xlabel('Wish list size (number of books)\n (log scale)', fontsize=16)
	plt.ylabel('Number of users \n (log scale)', fontsize=16)
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote plot " + out_filename)

def plot_give_away_list_size_distribution(plot_path, itemlist_size):
	out_filename = "giveawaylist_length.pdf"
	plt.close('all')

	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	[itemlist_lengths, frequency] = get_binning_of_values(itemlist_size)
	plt.scatter(itemlist_lengths, frequency,  s=30, linewidths=0, c=(0.0, 0.4470, 0.7410), alpha=0.8)
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.ylim([1.0, 10 ** 5])
	plt.xlim([1.0, 10 ** 6])
	plt.xlabel('Give-away list size (number of books)\n (log scale)', fontsize=16)
	plt.ylabel('Number of users \n (log scale)', fontsize=16)
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
	plt.ylim([1.0, 10 ** 7])
	plt.xlim([1.0, 10 ** 4])
	plt.xlabel('Number of different give-away lists that a book appears in \n ("have" popularity)\n (log scale)', fontsize=16)
	plt.ylabel('Number of books \n (log scale)', fontsize=16)
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
	plt.ylim([1.0, 10 ** 7])
	plt.xlim([1.0, 10 ** 4])
	plt.xlabel('Number of different wish lists that a book appears in \n ("wish" popularity)\n (log scale)', fontsize=16)
	plt.ylabel('Number of books \n (log scale)', fontsize=16)
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote plot " + out_filename)


########################################################################################################################
################################################# BOXPLOTS #############################################################
########################################################################################################################
# function for setting the colors of the box plots pairs

def plot_price_information(input_path):
	[filledOriginal, filledRepaired, prunedOriginal, prunedRepaired, data_pruned_original] = read_data_for_boxplots(input_path)
	original_price_distribution_plot(plot_path, data_pruned_original)
	# Here it takes a lot of time
	plot_boxplots(plot_path, filledOriginal, filledRepaired, prunedOriginal, prunedRepaired)

def read_data_for_boxplots(input_path):
	data_filled_original = pickle.load(open(input_path + "filled_original_inverted_lists.pickle", "rb"))
	data_pruned_original = pickle.load(open(input_path + "pruned_original_inverted_lists.pickle", "rb"))
	data_pruned_repaired = pickle.load(open(input_path + "pruned_repaired_inverted_lists.pickle", "rb"))
	data_filled_repaired = pickle.load(open(input_path + "filled_repaired_inverted_lists.pickle", "rb"))

	filledOriginal = list(data_filled_original[0].values())
	filledRepaired = list(data_filled_repaired[0].values())
	prunedOriginal = list(data_pruned_original[0].values())
	prunedRepaired = list(data_pruned_repaired[0].values())

	return [filledOriginal, filledRepaired, prunedOriginal, prunedRepaired, data_pruned_original]

def setBoxColors(bp):
	plt.setp(bp['boxes'][0], color=(0, 0.4470, 0.7410), alpha=0.9)
	plt.setp(bp['caps'][0], color=(0, 0.4470, 0.7410), alpha=0.9)
	plt.setp(bp['caps'][1], color=(0, 0.4470, 0.7410), alpha=0.9)
	plt.setp(bp['whiskers'][0], color=(0, 0.4470, 0.7410), alpha=0.9)
	plt.setp(bp['whiskers'][1], color=(0, 0.4470, 0.7410), alpha=0.9)
	plt.setp(bp['fliers'][0], color=(0, 0.4470, 0.7410), alpha=0.9)
	plt.setp(bp['medians'][0], color="#0B2E59", linewidth=2, alpha=0.8)

	plt.setp(bp['boxes'][1], color=(0.6350, 0.0780, 0.1840), alpha=0.9)
	plt.setp(bp['caps'][2], color=(0.6350, 0.0780, 0.1840), alpha=0.9)
	plt.setp(bp['caps'][3], color=(0.6350, 0.0780, 0.1840), alpha=0.9)
	plt.setp(bp['whiskers'][2], color=(0.6350, 0.0780, 0.1840), alpha=0.9)
	plt.setp(bp['whiskers'][3], color=(0.6350, 0.0780, 0.1840), alpha=0.9)
	plt.setp(bp['fliers'][1], color=(0.6350, 0.0780, 0.1840), alpha=0.9)
	plt.setp(bp['medians'][1], color='#630000', linewidth=2, alpha=0.8)


def plot_boxplots(plot_path, filledOriginal, filledRepaired, prunedOriginal, prunedRepaired):
	out_filename = "price_distribution.png"

	filledOriginal[:] = [x / 100.0 for x in filledOriginal]
	filledRepaired[:] = [x / 100.0 for x in filledRepaired]
	prunedOriginal[:] = [x / 100.0 for x in prunedOriginal]
	prunedRepaired[:] = [x / 100.0 for x in prunedRepaired]

	A = [filledOriginal, filledRepaired]
	B = [prunedOriginal, prunedRepaired]

	plt.hold(True)

	# first boxplot pair
	bp = plt.boxplot(A, positions = [2, 3], widths = 0.6, patch_artist=True)
	setBoxColors(bp)

	# second boxplot pair
	bp = plt.boxplot(B, positions = [5, 6], widths = 0.6, patch_artist=True)
	setBoxColors(bp)

	# set axes limits and labels
	plt.xlim(0,8)
	plt.ylim([0.001, 10**9])
	plt.yscale('log', nonposy='clip')
	plt.xticks([2.5, 5.5], ['Filled prices', 'Pruned prices'], fontsize = 13)
	plt.ylabel('Book price in USD \n (log scale)', fontsize=16)
	plt.xlabel('Price categories', fontsize=16)
	plt.title('Book price distribution, \n depending on the type of procesing', fontsize=18)
	plt.gca().yaxis.grid(True)

	# draw temporary red and blue lines and use them to create a legend
	hB, = plt.plot([1,1], color=(0, 0.4470, 0.7410), linewidth=2)
	hR, = plt.plot([1,1], color=(0.6350, 0.0780, 0.1840), linewidth=2)
	plt.legend((hB, hR),('Original prices', 'Corrected prices'))
	hB.set_visible(False)
	hR.set_visible(False)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote plot " + out_filename)


def original_price_distribution_plot(plot_path, data_pruned_original):
	out_filename = "price_frequency_scatter_for_orig_prices.pdf"

	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	prunedOriginal = list(data_pruned_original[0].values())
	prunedOriginal[:] = [log(x / 100.0) for x in prunedOriginal]
	[prices, frequency] = get_binning_of_values(prunedOriginal, True)
	xmin = min(prices)
	xmax = max(prices)
	ymin = min(frequency)
	ymax = max(frequency)
	plt.scatter(prices, frequency, s=30, linewidths=0, c=(0.9290, 0.6940, 0.1250), alpha=0.8)#(prices, frequency, bins='log', cmap=plt.cm.YlOrRd_r)
	plt.axis([xmin, xmax, ymin, ymax])
	plt.xlabel('Book value in USD \n (log scale)', fontsize=16)
	plt.ylabel('Number of books \n (log scale)', fontsize=16)
	cb = plt.colorbar()
	cb.set_label('counts')
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote plot " + out_filename)



if __name__ == '__main__':
	plot_path = "output/bookmooch/"
	input_path = "data-files/bookmooch/"

	[givers_sorted, receivers_sorted] = get_giver_and_receiver_frequency(input_path)

	plot_book_givers_cdf(plot_path, givers_sorted)
	plot_book_receivers_cdf(plot_path, receivers_sorted)


	[wishlist_size, itemlist_size, number_of_times_in_itemlist, number_of_times_in_wishlist] = get_data(input_path)

	plot_wish_list_size_distribution(plot_path, wishlist_size)
	plot_give_away_list_size_distribution(plot_path, itemlist_size)
	plot_item_have_popularity(plot_path, number_of_times_in_itemlist)
	plot_item_wish_popularity(plot_path, number_of_times_in_wishlist)

	# This will take a lot of time
	#plot_price_information(input_path)

