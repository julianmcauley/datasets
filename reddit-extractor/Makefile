# Version of python
PY=python
# Path to folder with scripts
PATH_SC=scripts
# Path to folder with plots
PATH_PL=plot
# Path to data (gameswap posts, success trades, acronyms...)
PATH_DATA=$(PATH_SC)/data
# Path to queries Giant Bomb
PATH_GB=$(PATH_DATA)/QueryGiantBomb
# Path to success trades
PATH_S=$(PATH_DATA)/success_threads
# Path to output dataset
PATH_OUT=$(PATH_SC)/dataset

# Input files
GB_FILES=$(PATH_GB)/games_giantbomb_1.json $(PATH_GB)/games_giantbomb_2.json $(PATH_GB)/games_giantbomb_3.json $(PATH_GB)/games_giantbomb_4.json $(PATH_GB)/games_giantbomb_5.json $(PATH_GB)/games_giantbomb_6.json $(PATH_GB)/games_giantbomb_7.json $(PATH_GB)/games_giantbomb_8.json $(PATH_GB)/games_giantbomb_9.json $(PATH_GB)/games_giantbomb_10.json $(PATH_GB)/success_gb.json
SUCCESS_FILES=$(PATH_S)/results-1nj197.json $(PATH_S)/results-21tfu8.json	$(PATH_S)/results-30t0rf.json $(PATH_S)/results-1qqksz.json	$(PATH_S)/results-21tggp.json	$(PATH_S)/results-30t0vc.json $(PATH_S)/results-1s95y8.json	$(PATH_S)/results-27atjl.json	$(PATH_S)/results-3ml5m1.json $(PATH_S)/results-1vv190.json	$(PATH_S)/results-2hthoh.json	$(PATH_S)/results-3mqb7x.json $(PATH_S)/results-1ycsij.json	$(PATH_S)/results-2htyl8.json
SORTED_SWAPS=$(PATH_DATA)/success_swap.txt
ACRONYMS=$(PATH_DATA)/acronyms.json
CONSOLE=$(PATH_DATA)/console_tags.txt
SUBISSIONS=$(PATH_DATA)/submissions.json
# Output files (dataset)
DATASET_GAMESWAP=$(PATH_OUT)/wishlist.json $(PATH_OUT)/itemlist.json $(PATH_OUT)/success.json

dataset: $(PATH_SC)/create_files.py $(PATH_SC)/utils_swapi.py $(PATH_SC)/roman.py $(SUBISSIONS) $(SORTED_SWAPS) $(GB_FILES)
	cd $(PATH_SC) && $(PY) create_files.py

info_dataset: $(DATASET_GAMESWAP) $(SUBISSIONS) $(SUCCESS_FILES)
	cd $(PATH_SC) && $(PY) statistics.py

histogram: $(PATH_PL)/histogram_levenshtein.m $(PATH_PL)/hist_lev.csv
	cd $(PATH_PL) && matlab -nodesktop -nosplash -nodisplay -r "histogram_levenshtein;quit"

plots: $(PATH_PL)/stat_plot.py $(DATASET_GAMESWAP)
	cd $(PATH_PL) && $(PY) stat_plot.py

success_swap_unsorted: $(PATH_SC)/crowdsourcing.py $(SUCCESS_FILES)
	cd $(PATH_SC) && $(PY) crowdsourcing.py

query_giantbomb: $(SORTED_SWAPS) $(SUBISSIONS) $(PATH_SC)/giantbomb/giantbomb.py
	cd $(PATH_SC) && $(PY) QueryGiantBomb.py
