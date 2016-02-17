#!/usr/bin/env python
__author__ = 'Dih0r'
import json
import matplotlib as mpl
import numpy as np
import math
mpl.use('TkAgg')
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re
import statistics
import datetime

def create_input_file_for_plots(input_path):
	with open(input_path + 'gameswap_submissions.json') as submissions:
		post_data = json.load(submissions)

	post_count_per_user = dict()

	for post in post_data:
			if post_count_per_user.get(post["author"], "none") == "none":
					post_count_per_user[post["author"]] = 1
			else:
					post_count_per_user[post["author"]] += 1

	sorted_by_number_of_posts = sorted(post_count_per_user.items(), key=lambda x: int(x[1]), reverse=True)

	list_of_number_of_posts = []
	for sorted_post in sorted_by_number_of_posts:
		list_of_number_of_posts.append(sorted_post[1])
	list_of_number_of_posts.sort()

	target = open(input_path + "statistics_reddit.txt", 'w')
	target.write(list_of_number_of_posts.__str__())
	target.write("\n")

	print("Wrote " + input_path + "statistics_reddit.txt\n")

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

	with open(input_path + "statistics_reddit.txt") as f:
		content = f.readlines()

	number_of_posts_per_user = list(map(int, content[0].replace("[", "").replace("]", "").split(",")))

	return number_of_posts_per_user

def plot_distribution_of_user_posting_activity(plot_path, number_of_posts_per_user):
	plot_name = "reddit_posts_per_user.pdf"

	plt.close('all')
	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	[posts_per_user, frequency] = get_binning_of_values(number_of_posts_per_user)
	plt.scatter(posts_per_user, frequency, s=30, linewidths=0, c=(0.0, 0.4470, 0.7410), alpha=0.8)
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.ylim([1.0, 10**5])
	plt.xlim([1.0, 10**3])
	plt.xlabel('Number of posts\n(log scale)', fontsize=16)
	plt.ylabel('Number of users \n(log scale)', fontsize=16)
	plt.grid(True)
	plt.savefig(plot_path + plot_name, bbox_inches='tight')
	plt.show()

	print("Wrote " + plot_name)

def plot_cdf_of_user_submissions(plot_path, number_of_posts_per_user):
	plot_name = 'reddit_sumbission_cdf.pdf'

	number_of_posts_per_user.sort(reverse=True)

	total_posts = sum(number_of_posts_per_user)

	percentage_of_posts = []
	for idx, val in enumerate(number_of_posts_per_user):
		if idx > 0:
			percentage_of_posts.append(float(float(val)/float(total_posts)) + float(percentage_of_posts[idx - 1]))
		else:
			percentage_of_posts.append(float(float(val)/float(total_posts)))
	index_vector = range(1, len(number_of_posts_per_user) + 1)

	plt.close('all')
	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	plt.plot(index_vector, percentage_of_posts, '-', color=(0.6350, 0.0780, 0.1840), linewidth=4)
	plt.yticks(np.arange(0, 1.1, 0.1))
	plt.ylim([0, 1.01])
	plt.xlim([0, len(index_vector)])
	plt.xlabel('Number Of Users', fontsize=16)
	plt.ylabel('Proportion of \nposts covered', fontsize=16)
	plt.grid(True)
	plt.savefig(plot_path + plot_name, bbox_inches='tight')
	plt.show()

	print("Wrote " + plot_name)

def plot_cdf_of_user_transactions(input_path, plot_path, number_of_posts_per_user):
	plot_name = 'reddit_transaction_cdf.pdf'

	with open(input_path + "reddit_successful_transactions.json", "r") as infile:
		data = json.load(infile)
		swap_freq = dict()
		for item in data:
			if item["user1"] not in swap_freq:
				swap_freq[item["user1"]] = 1
			else:
				swap_freq[item["user1"]] += 1

			if item["user2"] not in swap_freq:
				swap_freq[item["user2"]] = 1
			else:
				swap_freq[item["user2"]] += 1


	givers_sorted = sorted(swap_freq.values(), reverse = True)

	total_num_of_transactions = sum(givers_sorted)
	percentage_of_giver_posts = []
	for idx, val in enumerate(givers_sorted):
		if idx > 0:
			percentage_of_giver_posts.append(float(float(val)/float(total_num_of_transactions)) + float(percentage_of_giver_posts[idx - 1]))
		else:
			percentage_of_giver_posts.append(float(float(val)/float(total_num_of_transactions)))

	index_vector = list(range(1, len(givers_sorted) + 1))

	plt.close('all')
	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	plt.plot(index_vector, percentage_of_giver_posts, '-', color=(0.6350, 0.0780, 0.1840), linewidth=3)
	plt.gca().yaxis.set_ticks(np.arange(0, 1.1, 0.1))
	plt.ylim([0, 1])
	plt.xlim([0, len(index_vector)])

	plt.xticks(np.arange(0, len(index_vector) + 10, math.floor(len(index_vector) * 0.2)))

	labels = ['0%', '20%', '40%', '60%', '80%', '100%']
	plt.gca().set_xticklabels(labels)

	labels = ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
	plt.gca().set_yticklabels(labels)

	plt.xlabel('Percentage of active users', fontsize=16)
	plt.ylabel('Percentage of transactions covered', fontsize=16)
	plt.grid(True)
	plt.savefig(plot_path + plot_name, bbox_inches='tight')
	plt.show()

	print("Wrote " + plot_name)

def put_in_counter_dictionary(key, dictionary):
	if dictionary.get(key, "none") == "none":
		dictionary[key] = 1
	else:
		dictionary[key] += 1

def percent(val, total):
	return (val * 100.0 / float(total))


def get_data_for_plots(input_path):
	with open(input_path + 'gameswap_submissions.json', 'r') as f:
		post_data = json.load(f)

	with open(input_path + 'ignore_list.json', 'r') as f:
		ignore_list = json.load(f)

	author_hash = dict()

	total_structured = 0
	unstructured_with_docs = 0
	short_body = 0

	for post in post_data:
		body_html = post["body_html"]
		author = post["author"]
		body = post["body"]

		soup = BeautifulSoup(body_html, "html.parser")

		tables = soup.findAll('tr')
		lists  = soup.findAll('ul')

		found_structure = False
		if len(tables) > 0 or len(lists) > 0:
			found_structure  = True
			total_structured += 1
			put_in_counter_dictionary(author, author_hash)

		found_link = False
		if not(found_structure):
			tokens = re.split('\.(?!\w)|(?<!\w)\.|;|,|\*|\[|\]|\(|\)|[\s]*|[\t]*|[\n]*|[\f]*|[\r]*', body)

			for token in tokens:
				if (token.find("http") != -1) and \
					 ((token.find("drive.google") != -1) or (token.find("docs.google") != -1) or (token.find("goo.gl") != -1)):
					found_link = True
					break

		if not(found_structure) and found_link:
			unstructured_with_docs += 1

		elif not(found_structure) and not(found_link):
			if len(body) < 300:
				short_body += 1

	return [post_data, total_structured, unstructured_with_docs, short_body, ignore_list, author_hash]



def plot_piechart_for_submission_structure(plot_path,
																					 post_data,
																					 total_structured,
																					 unstructured_with_docs,
																					 short_body,
																					 author_hash,
																					 ignore_list):

	labels = 'Structured body \n content', 'Data stored in \n Google docs', 'Small-length body', 'Body with \n unstructured content'
	sizes = [percent(total_structured, len(post_data)),
					 percent(unstructured_with_docs, len(post_data)),
					 percent(short_body, len(post_data)),
					 (100.0 - (percent(total_structured, len(post_data))
										 + percent(unstructured_with_docs, len(post_data))
										 + percent(short_body, len(post_data))))]

	colors=['#798790',
					'#A9396B',
					'#D15D66',
					'#D6B588']

	explode = (0, 0.1, 0.1, 0.1) #only "explode" the 2nd slice (i.e. 'Hogs')
	plt.close('all')
	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top

	plt.pie(sizes,
					explode=explode,
					labels=labels,
					colors=colors,
					autopct='%1.1f%%',
					shadow=True,
					startangle=90)

	# Set aspect ratio to be equal so that pie is drawn as a circle.
	plt.axis('equal')
	plt.savefig(plot_path + 'structured_input_statistics.pdf')
	plt.show()


	print("Number of distinct authors with structured plot: "
				+ str(len(author_hash))
				+ ". Out of these, "
				+ str(len(set.intersection(set(ignore_list.keys()), set(author_hash.keys()))))
				+ " are on the ignore list.")

	print(str(percent(total_structured, len(post_data))) + "% of posts have structured input in the body.")



def get_running_average(input_path, window_size):

	with open(input_path + 'gameswap_submissions.json') as submissions:
			post_data = json.load(submissions)
	print("Data size: ", len(post_data))
	body_content_length = []
	running_average = []
	index_date = []
	for post in post_data:
		body = post["body"]
		body_content_length.append(len(body))
		index_date.append(datetime.datetime.fromtimestamp(int(float(post['created_utc']))).strftime('%b-%Y'))


	for ind, val in enumerate(body_content_length):
		if ind + window_size > len(body_content_length):
			break
		running_average.append(statistics.median(body_content_length[ind : ind + window_size - 1]))

	print(len(running_average))
	print(len(body_content_length))

	return [running_average, index_date, body_content_length]


def plot_running_median_of_post_length_in_time(plot_path, running_average, index_date):

	out_filename = "running_median_of_post_length_in_time.pdf"

	index = range(1, len(running_average) + 1)
	fit = np.polyfit(index, running_average, 1)
	fit_fn = np.poly1d(fit)

	plt.close('all')
	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	plt.plot(index, running_average, '.', color=(0.9290, 0.6940, 0.1250))
	plt.plot(index, fit_fn(index), '-', color=(0.6350, 0.0780, 0.1840), linewidth=3)
	plt.xlabel('Time \n (date at which the median of the considered window was posted)', fontsize=16)
	plt.ylabel('Body of post content length', fontsize=16)
	indices = list(np.arange(4000, len(running_average) + 1, int(len(running_average)/6)))
	plt.xticks(indices, list((index_date[i + 750] for i in indices)))
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote " + out_filename)

def plot_body_length_distribution(plot_path, body_content_length):
	out_filename = "scatterplot_body_content_length.pdf"

	plt.close('all')
	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	[body_length, frequency] = get_binning_of_values(body_content_length)
	plt.scatter(body_length, frequency,  s=30, linewidths=0, c=(0.0, 0.4470, 0.7410), alpha=0.6)
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.ylim([1.0, 10**3])
	plt.xlim([1.0, 10**5])
	plt.xlabel('Content length \n (log scale)', fontsize=16)
	plt.ylabel('Number of posts \n (log scale)', fontsize=16)
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote " + out_filename)


def load_json(fn):
	with open(fn) as f:
		data = json.load(f)

	game_list = []
	user_list = []
	data_dict = {}
	for d in data:
		uid = int(d['user_id'])
		user_list.append(uid)
		for g in d['game_id']:
			if not uid in data_dict:
				data_dict[uid] = []
			gid = int(g)
			data_dict[uid].append(gid)
			game_list.append(gid)
		user_list.append(uid)

	game_list = list(set(game_list))
	user_list = list(set(user_list))

	return data_dict, game_list, user_list


def nb_of_time_in_list(data, dict_list):
	data = set(data)

	len_list = []
	for d in data:
		cnt = 0
		for k,v in dict_list.items():
			if d in v:
				cnt += 1
		len_list.append(cnt)

	return len_list

def get_lists_size(dict_list):
	list_len = []
	for k,v in dict_list.items():
		list_len.append(len(v))
	return list_len

def plot_give_away_list_size_distribution(plot_path, have_dict):
	out_filename = "giveawaylist_length.pdf"

	[itemlist_lengths, frequency] = get_binning_of_values(get_lists_size(have_dict))

	plt.close('all')
	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	plt.scatter(itemlist_lengths, frequency,  s=30, linewidths=0, c=(0.0, 0.4470, 0.7410), alpha=0.8)
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.ylim([1.0, 10**3])
	plt.xlim([1.0, 10**5])
	plt.xlabel('Give-away list size (number of games) \n (log scale)', fontsize=16)
	plt.ylabel('Number of users \n(log scale)', fontsize=16)
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote " + out_filename)

def plot_wish_list_size_distribution(plot_path, wish_dict):
	out_filename = "wishlist_length.pdf"

	[wishlist_lengths, frequency] = get_binning_of_values(get_lists_size(wish_dict))

	plt.close('all')
	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	plt.scatter(wishlist_lengths, frequency,  s=30, linewidths=0, c=(0.0, 0.4470, 0.7410), alpha=0.8)
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.ylim([1.0, 10 ** 3])
	plt.xlim([1.0, 10 ** 5])
	plt.xlabel('Wish list size (number of games) \n (log scale)', fontsize=16)
	plt.ylabel('Number of users \n(log scale)', fontsize=16)
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote " + out_filename)


def plot_item_have_popularity(plot_path, have_game, have_dict):
	out_filename = "giveaway_item_popularity.pdf"

	[have_popularity, frequency] = get_binning_of_values(nb_of_time_in_list(have_game, have_dict))

	plt.close('all')
	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	plt.scatter(have_popularity, frequency, s=30, linewidths=0, c=(0.9290, 0.6940, 0.1250), alpha=0.8)
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.ylim([1.0, 10 ** 2])
	plt.xlim([1.0, 10 ** 3])
	plt.xlabel('Number of different give-away lists that a game appears in \n ("have" popularity)  \n (log scale)', fontsize=16)
	plt.ylabel('Number of games \n(log scale)', fontsize=16)
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote " + out_filename)

def plot_item_wish_popularity(plot_path, wish_game, wish_dict):
	out_filename = "wishitem_popularity.pdf"

	[have_popularity, frequency] = get_binning_of_values(nb_of_time_in_list(wish_game, wish_dict))

	plt.close('all')
	fig = plt.figure()
	fig.canvas.manager.window.attributes('-topmost', 1) #put widow on top
	plt.scatter(have_popularity, frequency, s=30, linewidths=0, c=(0.9290, 0.6940, 0.1250), alpha=0.8)
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.ylim([1.0, 10 ** 2])
	plt.xlim([1.0, 10 ** 3])
	plt.xlabel('Number of different give-away lists that a game appears in \n ("wish" popularity)  \n (log scale)', fontsize=16)
	plt.ylabel('Number of games \n(log scale)', fontsize=16)
	plt.grid(True)
	plt.savefig(plot_path + out_filename, bbox_inches='tight')
	plt.show()

	print("Wrote " + out_filename)


if __name__ == '__main__':

	input_path = "data-files/reddit/"

	plot_path = "output/reddit/"

	create_input_file_for_plots(input_path)

	number_of_posts_per_user = get_data(input_path)

	plot_distribution_of_user_posting_activity(plot_path, number_of_posts_per_user)

	plot_cdf_of_user_submissions(plot_path, number_of_posts_per_user)

	plot_cdf_of_user_transactions(input_path, plot_path, number_of_posts_per_user)

	#################### Statistics for post body structure #########################################
	[post_data, total_structured, unstructured_with_docs, short_body, ignore_list, author_hash] = get_data_for_plots(input_path)

	plot_piechart_for_submission_structure(plot_path,
																				 post_data,
																				 total_structured,
																				 unstructured_with_docs,
																				 short_body,
																				 author_hash,
																				 ignore_list)

	print("Pieplot done.")


	######################################## Reddit body length stats ###############################
	window_size = 1500

	[running_average, index_date, body_content_length] = get_running_average(input_path, window_size)

	plot_running_median_of_post_length_in_time(plot_path, running_average, index_date)

	plot_body_length_distribution(plot_path, body_content_length)



	######################################## Normal statistics ###############################


	have_file = input_path + "itemlist.json"
	wish_file = input_path + "wishlist.json"

	# Load a dict of data
	# Key is the user_id
	have_dict, have_game, have_user = load_json(have_file)
	wish_dict, wish_game, wish_user = load_json(wish_file)

	print("Wish data points[tot/game/user]:", str(len(wish_game)), str(len(set(wish_game))), str(len(set(wish_user))))
	print("Have data points[tot/game/user]:", str(len(have_game)), str(len(set(have_game))), str(len(set(have_user))))


	plot_path = "output/reddit/"
	plot_give_away_list_size_distribution(plot_path, have_dict)
	plot_wish_list_size_distribution(plot_path, wish_dict)
	plot_item_have_popularity(plot_path, have_game, have_dict)
	plot_item_wish_popularity(plot_path, wish_game, wish_dict)



	print("Done writing figures.")
