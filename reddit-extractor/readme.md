This file details the differents files and their use in the optional semester project named: Swapi - A swapping recommender system. The goal is to Extract a dataset for Swapi.

A makefile with rules to create the dataset, plots and others files was created. 
Makefile
	dataset: 				Create final dataset (wish list, item list, success swaps)
	info_dataset:			Print information about the dataset (number of games, number of users...)
	histogram:				Create histogram of Levensthein distance
	plots:					Create plots on wish list and item list sizes and games popularity 
	success_swap_unsorted:	Do a preliminary sort of the success trades, this file is destined to be sorted manually  
	query_giantbomb:		Query GiantBomb with extracted games names from posts and success trades (this take several hours because the API limits to 1 query/second)

File structure:
Report
	Presentation.pdf:	PDF copy of the presentation
	Report:				PDF copy of the report

plot
	giveAwayItemPopularity.pdf:	Plot of the "have" popularity (From final dataset)
	giveAwayListLength.pdf:		Plot of the Give-away list size (From final dataset)
	haveItemPopularity.pdf:		Plot of the "wish" popularity (From final dataset)
	wishListLength.pdf: 		Plot of the wish list size (From final dataset)
	stat_plot.py:				Scripts that create the 4 preceding plots

	histogram_lev.pdf:			Histogram of Levenshtein distance
	hist_lev.csv:				CSV file with Levenshtein distance between games and query
	histogram_levenshtein.m:	Matlab script to make histogram_lev.pdf

scripts
	data
		acronyms.json:		Dictionary of acronyms
		console_tags.txt:	File containing consoles mentioned in posts
		submission.json:	Output of the Gameswap crawler, contains all posts
		success_swap.txt:	File that was manually sorted (successful swaps)
		success_threads/* :	Output of the success trade threads crawler
		QueryGiantBomb/* : 	Contains tuples query - answer from giantbomb for all games names 						extracted from posts

	giantbomb/* : giantbomb API

	dataset (final dataset)
		game_gameid.json:	Contains game - game id pairs
		game_gameid.txt:	Contains game - game id pairs
		query_gameid.json:	Contains query - game id pairs
		query_gameid.txt:	Contains query - game id pairs
		user_userid.json:	Contains user - user id pairs
		user_userid.txt:	Contains user - user id pairs
		itemlist.json:		Final dataset: Contains users' itemlists
		wishlist.json:		Final dataset: Contains users' wishlist
		success.json:		Final dataset: Contains successful swaps

	others
		Contains files that were created during experiments and are not used to generate the final dataset
