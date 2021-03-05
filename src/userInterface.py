# Author: Christoffer Eid
# CE223AF@STUDENT.LNU.SE
# Teacher: Ilir Jusufi
from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from tkinter import ttk
from tkinter import simpledialog
import tkinter as tk
import storesDb
import time

# Connection info
cnx = mysql.connector.connect(user='root', password='dGX!f&^HTo5h36',
                               host='127.0.0.1')
cursor  = cnx.cursor()
DB_NAME = 'StoreDatabase'
cursor.execute("USE {}".format(DB_NAME))

def delete():
    # Used when creating a tree to make sure there's no other tree left.
    for row in tree.get_children():
        tree.delete(row)
    
def createTree(headingsList):
    # Creates a tree based on headings from headingsList.
    delete()
    tree["columns"] = tuple(range(len(headingsList)))
    for count, heading in enumerate(headingsList):
        tree.column(f"#{count+1}", width=round(400/len(headingsList)), anchor=tk.CENTER)
        tree.heading(f"#{count+1}", text=heading)
    tree.pack()

# QUERIES
#
def queryAvgAge():
    cursor.execute("""
        SELECT AVG(Customers.age), Stores.name 
        FROM Customers 
        INNER JOIN ordersandarticles 
        ON customerid=ordersandarticles.customer 
        INNER JOIN Stores 
        ON ordersandarticles.store=Stores.storeid 
        GROUP BY Stores.name 
        ORDER BY AVG(Customers.age);
        """)

def queryStores():
    cursor.execute("""
        SELECT name, address 
        FROM Stores 
        ORDER BY name;""")

def queryCustomerCount():
    cursor.execute("""
        SELECT COUNT(customer), Stores.name 
        FROM ordersandarticles 
        INNER JOIN Stores 
        ON ordersandarticles.store=Stores.storeid 
        GROUP BY Stores.name 
        ORDER BY COUNT(customer);
        """)

def queryHowMuch(articleid):
    if articleid in range(1, 101):
        cursor.execute(f"""
            SELECT name, price 
            FROM Articles 
            WHERE articleid={articleid};""")

def queryOrder(orderid):
    if orderid in range(1, 201):
        cursor.execute(f"""
            SELECT orderid, Customers.firstname, Customers.lastname 
            FROM ordersandarticles 
            INNER JOIN Customers 
            ON customer=Customers.customerid 
            WHERE orderid = {orderid}
            GROUP BY orderid 
            ORDER BY orderid;
        """)

def queryShoppingCart(orderid):
    if orderid in range(1, 201):
        cursor.execute(f"""
            SELECT name, price, amount 
            FROM ordersandarticles 
            WHERE orderid = {orderid} 
            ORDER BY name;
            """)


#FUNCTIONS FOR BUTTONS
#
def stores():
    createTree(["Store", "Address"])
    queryStores()
    for row in cursor:
        tree.insert("", tk.END, values=row)        

def averageAge():
    createTree(["Average age", "Store"])
    queryAvgAge()
    for row in cursor:
        tree.insert("", tk.END, values=row)        

def customerCount():
    createTree(["Amount of customers", "Store"])
    queryCustomerCount()
    for row in cursor:
        tree.insert("", tk.END, values=row)        

def checkArticle():
    createTree(["Product", "Price"])
    USER_INP = simpledialog.askinteger(title="Article ID",
                                  prompt="Enter a value (1-100)")
    queryHowMuch(USER_INP)
    for row in cursor:
        tree.insert("", tk.END, values=row)        

def checkOrder():
    createTree(["Order ID", "First Name", "Surname"])
    USER_INP = simpledialog.askinteger(title="Order ID",
                                  prompt="Enter a value (1-200)")
    queryOrder(USER_INP)
    for row in cursor:
        tree.insert("", tk.END, values=row)        

def checkShoppingCart():
    createTree(["Article", "Price per (sek)", "Amount"])
    USER_INP = simpledialog.askinteger(title="Order ID",
                                  prompt="Enter a value (1-200)")
    queryShoppingCart(USER_INP)
    for row in cursor:
        tree.insert("", tk.END, values=row)

# User interface
root = tk.Tk()
root.title("Ica Maxü Retail Store Database")
root.geometry("1000x800")
root.grid()

# Table
tree = ttk.Treeview(root, columns=(1), show='headings')
tree.pack(side='right', fill='y')
tree.column("#1", width=400)

# Buttons
button1 = tk.Button(text="Stores", command=stores)
button1.pack(pady=10)
button2 = tk.Button(text="Average age of customer per store", command=averageAge)
button2.pack(pady=10)
button3 = tk.Button(text="Total amount of customers per store", command=customerCount)
button3.pack(pady=10)
button4 = tk.Button(text="Check Article", command=checkArticle)
button4.pack(pady=10)
button5 = tk.Button(text="Check Orderer", command=checkOrder)
button5.pack(pady=10)
button6 = tk.Button(text="Check Shopping Cart", command=checkShoppingCart)
button6.pack(pady=10)

root.mainloop()

cnx.commit()
cursor.close()
cnx.close()