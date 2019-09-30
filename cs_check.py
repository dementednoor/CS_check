import os
import binascii
import sqlite3
from termcolor import colored
import re
import unittest

def poll(start_message: object) -> object:
    answer = input(start_message)
    if answer == "y":
        flag = True
    elif answer == "n":
        flag = False
    else:
        poll("Please enter y or n\n")
    while flag:
        if answer == "y":
            try:
                new_path = input("Input the new path for arrays\n")
                os.chdir(new_path)
            except FileNotFoundError:
                os.chdir(def_path)
            #  print("the new path for arrays is {}".format(def_path))
            return "y"
        else:
            return "n"


def db_re(value, pattern):
    pat = re.compile("({}.*)".format(pattern))
    return pat.search(value) is not None


def_path = "/home/noor/u55/u55_lpack/"
os.chdir(def_path)
poll(("Current path is {}. Do you want to change it? (y/n)\n".format(os.getcwd())))
print("So the path is {}".format(os.getcwd()))

#  cursor.execute("""CREATE TABLE u55_arrays (title text, csum text)""")

list_of_pairs = []
for i in os.listdir(def_path):
    print(i)
    try:
        with open(i, 'rb') as f:
            bin_file = f.read()
            c_sum = binascii.crc32(bin_file)
            print("file - {}, CS - {}\n".format(i, c_sum))
            t = (i, c_sum)  # tuple array - control sum
            list_of_pairs.append(t)
    except IsADirectoryError:
        continue
print("{} \n".format(list_of_pairs))
conn = sqlite3.connect("u55.db")  # connection
cursor = conn.cursor()  # курсор (указатель) на бд
conn.create_function("REGEXP", 2, db_re)
#  cursor.executemany("""INSERT INTO u55_arrays VALUES (?, ?)""", list_of_pairs)
check_path = "/home/noor/u55_massives/u55_lpack-master/"
first = os.listdir(check_path)[0]

# starting the cycle
for checkable_file in os.listdir(check_path):
    query = "SELECT csum FROM u55_arrays WHERE title = ?"
    cursor.execute(query, [checkable_file])
    try:
        with open(checkable_file, 'rb') as f:
            file = f.read()
            c_sum = binascii.crc32(file)
            #  print(type(c_sum))
            db_cs = int(cursor.fetchone()[0])
            print("Checking: {}\nThe database CS = {}, Your CS = {}".format(checkable_file ,db_cs, c_sum))
            #  print(type(cursor.fetchone()[0]))
            print(colored("CS's are equal \n", 'green')) if db_cs == c_sum else \
                print(colored("CS's are not equal!\n", 'red'))
    except FileNotFoundError:
        q = 'SELECT title FROM u55_arrays WHERE REGEXP(title, ?)'
        cursor.execute(q, ('kpa', ))
        alt = cursor.fetchone()[0]  # alternative
        #  print(colored("A match found: {}\n".format(alt), 'magenta'))
        print(colored("File {} is not found.\nWanna check {} instead? (y/n)\n", 'red').format(checkable_file, alt))

        while True:
            answer = input()
            if answer == "y" or answer == "n":
                break
        if answer == "n":
            continue
        elif answer == "y":
            alt_cs_q = "SELECT csum FROM u55_arrays WHERE title = ?"
            cursor.execute(alt_cs_q, [alt]) # alternative control sum query
            with open(check_path + '/' + checkable_file, 'rb') as f:
                file = f.read()
                c_sum = binascii.crc32(file)
                db_cs = cursor.fetchone()[0]
                print("Checking: {}\nThe database CS = {}, Your CS = {}".format(alt, db_cs, c_sum))
                print(colored("CS's are equal \n", 'green')) if db_cs == c_sum else \
                    print(colored("CS's are not equal!\n", 'red'))
            #  answer = input("Press 'y' or 'n'")
    conn.commit()
cursor.close()
