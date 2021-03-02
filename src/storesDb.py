import mysql.connector
import csv


# Connection info
cnx = mysql.connector.connect(user='root', password='dGX!f&^HTo5h36',
                               host='127.0.0.1')
cursor  = cnx.cursor()
DB_NAME = 'Stores'

# Source: https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

# Function to create a list from .csv-file.
# Source: https://docs.python.org/3/library/csv.html
def createList(file):
    table = []
    with open(file, newline='') as csvfile:
        column = csv.reader(csvfile)
        for row in column:
            table.append(row)
    return table

# Fill Article table from list
# Skipping first entry as we dont want headlines as entries.
def fillArticleTable(articleList):
    for i in articleList[1:]:
        cursor.execute(f"""
        INSERT INTO 
            Articles(name, price(sek)) 
            VALUES({i[0]}, {i[1]})""")

# Fill Customer table from list
# Skipping first entry as we dont want headlines as entries.
def fillCustomerTable(customerList):
    for i in customerList[1:]:
        cursor.execute(f"""
        INSERT INTO 
            Customers(number, firstname, lastname, gender, age) 
            VALUES({i[0]}, {i[1]}, {i[2]}, {i[3]}, {i[4]})""")

# Fill Store table from list
# Skipping first entry as we dont want headlines as entries.
def fillStoreTable(storeList):
    for i in storeList[1:]:
        cursor.execute(f"""
        INSERT INTO 
            Stores(number, name, address) 
            VALUES({i[0]}, {i[1]}, {i[2]})""")


# Tables are stored in a dictionary where, tablename becomes the key and
# 'output' becomes the value.
TABLES = {}

# The Customer table
# Personal number as primary key.
TABLES['Customers'] = ("""
    CREATE TABLE `Customers`(
        `number` BIGINT NOT NULL, 
        `firstname` varchar(50), 
        `lastname` varchar(50), 
        `gender` varchar(1), 
        `age` TINYINT, 
        PRIMARY KEY (`number`)) 
    ENGINE=InnoDB""")

# The Articles table
# Article number as primary key. 
# Article number gets auto incremented.
TABLES['Articles'] = ("""
    CREATE TABLE `Articles`(
        `number` SMALLINT NOT NULL AUTO_INCREMENT, 
        `name` varchar(100), 
        `price` TINYINT, 
        PRIMARY KEY (`number`))
    ENGINE=InnoDB""")

# The Stores table
# Organisation number as primary key.
TABLES['Stores'] = ("""
    CREATE TABLE `Stores`(
        `number` BIGINT NOT NULL, 
        `name` varchar(250), 
        `address` varchar(250), 
        PRIMARY KEY (`number`))
    ENGINE=InnoDB""")

# The Orders table. 
# If entry for stores is removed. The order will be removed.
# If entry for Customer is removed. The customer will be set to null.
# Entry for Order detail
TABLES['Orders'] = ("""
    CREATE TABLE `Orders`(
        `number` INT NOT NULL AUTO_INCREMENT, 
        `store` BIGINT NOT NULL, 
        `customer` BIGINT, 
        `ordersarticles` INT NOT NULL, 
        PRIMARY KEY (`number`,`store`), 
        FOREIGN KEY (`store`) 
            REFERENCES `Stores`(`number`) 
            ON DELETE CASCADE, 
        FOREIGN KEY (`customer`) 
            REFERENCES `Customers`(`number`) 
            ON DELETE SET NULL, 
        FOREIGN KEY (`ordersarticles`) 
            REFERENCES `OrdersArticles`(`number`)) 
    ENGINE=InnoDB""")

# Table for OrdersArticles
# Connects orders with its articles in line with BCNF. 
# Order as foreign key. If order is removed, all OrderArticles
# connected to it, are removed.
# Article as foreign key. If an article is removed. All its
# connected OrderArticles are removed. 
TABLES['OrdersArticles'] = ("""
    CREATE TABLE `OrderDetail`(
        `number` INT NOT NULL AUTO_INCREMENT, 
        `order` INT NOT NULL, 
        `article` INT NOT NULL, 
        PRIMARY KEY (`number`), 
        FOREIGN KEY (`order`)
            REFERENCES `Orders`(`number`)
            ON DELETE CASCADE, 
        FOREIGN KEY (`article`)
            REFERENCES `Articles`(`number`)
            ON DELETE CASCADE))
    ENGINE=InnoDB""")