import mysql.connector
from mysql.connector import errorcode
# If slow, try to use MySQLdb instead of mysql (http://mysql-python.sourceforge.net/MySQLdb.html)


# Configuration of the MySQL database
config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'gameswap',
    'raise_on_warnings': True,
}


# Create tables
def create_tables(db):
    TABLES = {}

    # Create table "user": |user_id|name|
    TABLES['user'] = (
        "CREATE TABLE `user` ("
        "  `user_id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `name` varchar(20) NOT NULL UNIQUE,"
        "  PRIMARY KEY (`user_id`)"
        ") ENGINE=InnoDB")

    # Create table "game": |game_id|name|
    TABLES['game'] = (
        "CREATE TABLE `game` ("
        "  `game_id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `name` varchar(50) NOT NULL UNIQUE,"
        "  PRIMARY KEY (`game_id`)"
        ") ENGINE=InnoDB")

    # Create table "have": |user_id|game_id|
    TABLES['have'] = (
        "CREATE TABLE `have` ("
        "  `user_id` int(11) NOT NULL,"
        "  `game_id` int(11) NOT NULL,"
        "  PRIMARY KEY (`user_id`, `game_id`),"
        "CONSTRAINT `have_ibfk_1` FOREIGN KEY (`user_id`)"
        "     REFERENCES `user` (`user_id`),"
        "CONSTRAINT `have_ibfk_2` FOREIGN KEY (`game_id`)"
        "     REFERENCES `game` (`game_id`)"
        ") ENGINE=InnoDB")

    # Create table "want": |user_id|game_id|
    TABLES['want'] = (
        "CREATE TABLE `want` ("
        "  `user_id` int(11) NOT NULL,"
        "  `game_id` int(11) NOT NULL,"
        "  PRIMARY KEY (`user_id`, `game_id`),"
        "CONSTRAINT `want_ibfk_1` FOREIGN KEY (`user_id`)"
        "     REFERENCES `user` (`user_id`),"
        "CONSTRAINT `want_ibfk_2` FOREIGN KEY (`game_id`)"
        "     REFERENCES `game` (`game_id`)"
        ") ENGINE=InnoDB")

    # Create tables
    cursor = db.cursor()
    for name, ddl in TABLES.iteritems():
        try:
            print("Creating table {}: ".format(name))
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()


# Connect to database
def connect_db():
    cnx = mysql.connector.connect(**config)
    return cnx


# Close connection
def close_db(cnx):
    cnx.close()


# Create new tuple in table "user"
def insert_user(cnx, user):
    tuple = (user,)
    try:
        cursor = cnx.cursor()
        add_user = ("INSERT INTO USER "
                    "(NAME) "
                    "VALUES (%s)")
        # Insert new user
        cursor.execute(add_user, tuple)
        cnx.commit()
        cursor.close()
    except mysql.connector.errors.IntegrityError as err:
        pass


# Create new tuple in table "game"
def insert_game(cnx, game):
    tuple = (game,)
    try:
        cursor = cnx.cursor()
        add_game = ("INSERT INTO GAME "
                    "(NAME) "
                    "VALUES (%s)")
        # Insert new game
        cursor.execute(add_game, tuple)
        cnx.commit()
        cursor.close()
    except mysql.connector.errors.IntegrityError as err:
        pass


# Get user_id from user name
def get_user_id(cnx, user_name):
    tuple = (user_name,)
    cursor = cnx.cursor()
    query = ("""SELECT user_id FROM user WHERE name = %s""")
    cursor.execute(query, tuple)
    user_id = (cursor.fetchone())
    if user_id is not None:
        user_id = user_id[0]
    cursor.close()
    return user_id


# Get game_id from game name
def get_game_id(cnx, game_name):
    tuple = (game_name,)
    cursor = cnx.cursor()
    query = ("""SELECT game_id FROM game WHERE name = %s""")
    cursor.execute(query, tuple)
    game_id = (cursor.fetchone())
    if game_id is not None:
        game_id = game_id[0]
    cursor.close()
    return game_id


# Drop table "user"
def delete_all_users(cnx):
    cursor = cnx.cursor()
    cursor.execute("DROP TABLE IF EXISTS user")
    cursor.close()
    print("Delete table user")


# Drop table "game"
def delete_all_games(cnx):
    cursor = cnx.cursor()
    cursor.execute("DROP TABLE game")
    cursor.close()
    print("Delete table game")
