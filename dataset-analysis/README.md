The **data-files** folder contains, in each subfolder, the input data collected from the platform whose name is referred.

1. **bookmooch**: the pickles contain [item_values, ul, wl, giveaway_lists, wishlists, _], where:
  * item_values is a dictionary keyed on the item id, having the value equal to the price of the book on Amazon (the price is for the used book)
  * ul is an inverted list keyed on item ids, with the value represented as the set of users owning the respective item
  * wl is an inverted list keyed on item ids, with the value represented as the set of users wishing for the respective item
  * itemlists is a dictionary keyed on the user ids, having as values a set of item ids, representing the owned items
  * wishlists is a dictionary keyed on the user ids, having as values a set of item ids, representing the desired items
The transac.csv file contains a transaction per line, under the form of giver_id, receiver_id, item_id, timestamp

2. **readitswapit**: users.json contains a list of user-objects and is fairly self-explanatory. The same goes for books.json. 
user_itersections.txt contains, per line, a pair of users whose reciprocal wishlist itemlist intersection is non void.

3. **swapacd**: users.json contains a list of user-objects and is fairly self-explanatory. The same goes for cds.json.

4. **swapadvd**: users.json contains a list of user-objects and is fairly self-explanatory. The same goes for dvds.json.

6. **reddit**: itemlist.json and wishlist.json contain each user and their associated list of wants and haves. 
reddit_successful_transactions.json contains the pairs of users who have transacted and their exchanged games. 
gameswap-submissions.json contains a list of all the posts in the /r/gameswap thread.


The **output** folder contains, similarly, the plots outputted resulted from running the scripts, per platform. 

Running each of the 5 scripts plot_bookmooch.py, plot_reddit.py, plot_swapacd.py, plot_swapadvd.py, plot_readitswapit.py,
will generate the associated plots for the distributions of various entities within the platforms (which can be referred
in the thesis). 
