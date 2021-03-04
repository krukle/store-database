from __future__ import print_function
import mysql.connector
import csv
from mysql.connector import errorcode
import random

# Connection info
cnx = mysql.connector.connect(user='root', password='dGX!f&^HTo5h36',
                               host='127.0.0.1')
cursor  = cnx.cursor(dictionary=True)
DB_NAME = 'StoreDatabase'

def create_database(cursor, DB_NAME):
    # Source: https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def createList(file):
    # Function to create a list from .csv-file.
    # Source: https://docs.python.org/3/library/csv.html
    table = []
    with open(file, newline='') as csvfile:
        column = csv.reader(csvfile)
        for row in column:
            table.append(row)
    return table

def fillArticleTable(articleList):
    # Fill Article table from list
    # Skipping first entry as we dont want headlines as entries.
    for i in articleList[1:]:
        cursor.execute(f"""
        INSERT INTO 
            `Articles` (`name`, `price`) 
            VALUES("{i[0]}", "{i[1]}")""")
def fillCustomerTable(customerList):
    # Fill Customer table from list
    # Skipping first entry as we dont want headlines as entries.
    for i in customerList[1:]:
        cursor.execute(f"""
        INSERT INTO 
            `Customers` (`firstname`, `lastname`, `gender`, `age`) 
            VALUES("{i[0]}", "{i[1]}", "{i[2]}", "{i[3]}")""")

def fillStoreTable(storeList):
    # Fill Store table from list
    # Skipping first entry as we dont want headlines as entries.
    for i in storeList[1:]:
        cursor.execute(f"""
        INSERT INTO 
            `Stores` (`name`, `address`) 
            VALUES("{i[0]}", "{i[1]}")""")

def randomOneToFive():
    # Generates a random number between 1-5 where 1 is the most usual outcome.
    n = random.randint(1, 10)
    if n > 5:
        n = 1
    return n

def generateOrdersTable(AMOUNT_OF_ORDERS, MAX_ARTICLES_BOUGHT):
    # Randomly generates orders to fill up `Orders` and `OrdersArticles`.
    for order in range(1, AMOUNT_OF_ORDERS+1):
        maxArticles = random.randint(1, MAX_ARTICLES_BOUGHT)
        customer = random.randint(1, 150)
        store    = random.randint(1, 4)

        cursor.execute(f"""
            INSERT INTO 
                `Orders` (`store`, `customer`)
                VALUES("{store}", "{customer}")
        """)

        for i in range(maxArticles):
            article  = random.randint(1, 100)
            cursor.execute(f"""
                INSERT INTO
                    `OrdersArticles` (`order`, `article`, `amount`)
                    Values("{order}", "{article}", "{randomOneToFive()}")
                """)

def viewOrdersArticles():
    # Creates a view for easier access between orders and articles.
    cursor.execute("""
        CREATE VIEW `ordersandarticles` AS 
            SELECT * FROM `Orders` 
            INNER JOIN `OrdersArticles` ON Orders.orderid=OrdersArticles.order 
            INNER JOIN `Articles` ON OrdersArticles.article=Articles.articleid;
        """)

def createTables():
    # Creates tables for 'Stores' database.
    # Tables are stored in a dictionary where, tablename becomes the key and
    # 'output' becomes the value.
    TABLES = {}

    # The Customer table
    # Personal id as primary key.
    TABLES['Customers'] = ("""
        CREATE TABLE `Customers`(
            `customerid` INT NOT NULL AUTO_INCREMENT, 
            `firstname` varchar(50), 
            `lastname` varchar(50), 
            `gender` varchar(1), 
            `age` TINYINT, 
            PRIMARY KEY (`customerid`)) 
        ENGINE=InnoDB""")

    # The Articles table
    # Article id as primary key. 
    # Article id gets auto incremented.
    TABLES['Articles'] = ("""
        CREATE TABLE `Articles`(
            `articleid` INT NOT NULL AUTO_INCREMENT, 
            `name` varchar(100), 
            `price` TINYINT, 
            PRIMARY KEY (`articleid`)) 
        ENGINE=InnoDB""")

    # The Stores table
    # Organisation id as primary key.
    TABLES['Stores'] = ("""
        CREATE TABLE `Stores`(
            `storeid` INT NOT NULL AUTO_INCREMENT, 
            `name` varchar(250), 
            `address` varchar(250), 
            PRIMARY KEY (`storeid`)) 
        ENGINE=InnoDB""")

    # The Orders table. 
    # If entry for stores is removed. The order will be removed.
    # If entry for Customer is removed. The customer will be set to null.
    # Entry for Order detail
    TABLES['Orders'] = ("""
        CREATE TABLE `Orders`(
            `orderid` INT NOT NULL AUTO_INCREMENT, 
            `store` INT NOT NULL, 
            `customer` INT NOT NULL, 
            PRIMARY KEY (`orderid`), 
            FOREIGN KEY (`customer`)
                REFERENCES `Customers` (`customerid`),
            FOREIGN KEY (`store`) 
                REFERENCES `Stores` (`storeid`)) 
        ENGINE=InnoDB""")

    # Table for OrdersArticles
    # Connects orders with its articles in line with BCNF. 
    # Order as foreign key. If order is removed, all OrderArticles
    # connected to it, are removed.
    # Article as foreign key. If an article is removed. All its
    # connected OrderArticles are removed. 
    TABLES['OrdersArticles'] = ("""
        CREATE TABLE `OrdersArticles`(
            `ordersarticlesid` INT NOT NULL AUTO_INCREMENT, 
            `order` INT NOT NULL, 
            `article` INT NOT NULL, 
            `amount` INT NOT NULL, 
            PRIMARY KEY (`ordersarticlesid`),
            FOREIGN KEY (`order`) 
                REFERENCES `Orders` (`orderid`),
            FOREIGN KEY (`article`)
                REFERENCES `Articles` (`articleid`)) 
        ENGINE=InnoDB""")
    return TABLES

# Tries to USE Database. If impossible, creates database instead. 
try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor, DB_NAME)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME

        TABLES = createTables()

        for table_name in TABLES:
            table_description = TABLES[table_name]
            print("Creating table {}: ".format(table_name))
            cursor.execute(table_description)

        customers = createList('docs/customers.csv')
        articles = createList('docs/articles.csv')
        stores = createList('docs/stores.csv')      

        fillStoreTable(stores)
        fillCustomerTable(customers)
        fillArticleTable(articles)
        
        generateOrdersTable(200, 10)
        viewOrdersArticles()
    else:
        print(err)
        exit(1)

cnx.commit()
cursor.close()
cnx.close()