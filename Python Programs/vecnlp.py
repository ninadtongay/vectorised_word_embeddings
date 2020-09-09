#!pip install faker
import pandas as pd
import sqlite3
import numpy as np
import pickle as pickle
import subprocess,io
from time import time
from sklearn.decomposition import PCA
from itertools import repeat
from faker import Faker
from sklearn.utils import shuffle

from get_word_vector import get_vector
from cosine_sim import cos_sim
from generate_data import get_data
from sel_fun import sel_func_post,sel_func_city
from sql_join import join_table_fun_city,join_table_fun_post
from accuracy import check_accuracy

#Getting Vectors for available posts
connection = sqlite3.connect("position_city_database_with_embeddings.db") 
crsr = connection.cursor() 
engineer_vector = get_vector('engineer')
manager_vector = get_vector('manager')
developer_vector = get_vector('developer')
ceo_vector = get_vector('ceo')
cto_vector = get_vector('cto')
coo_vector = get_vector('coo')
waiter_vector = get_vector('waiter')

#Getting Vectors for available cities
victoria_vector = get_vector('victoria')
vancouver_vector = get_vector('vancouver')
delhi_vector = get_vector('delhi')
pune_vector = get_vector('pune')
ottawa_vector = get_vector('ottawa')
toronto_vector = get_vector('toronto')
mumbai_vector = get_vector('mumbai')

#Getting input size
n1 = int(input("Enter number of rows for table containing Name,Post and City: "))
n2 = int(input("Enter number of rows for table containing Post and City: "))
get_data(n1,n2)
choice= (input("Please enter choice (City/Post):"))
if choice == 'City':
    city = input("Enter the city name:") # vancouver
    thresh = int(input("Enter the threshold between 0-1:"))
    join_list = sel_func_city(city, thresh,0) # Getting locations which having similarity score of more than .85 with 'Victoria'
    queryc = join_table_fun_city(join_list)
    tic = time()
    #Query for city
    crsr.execute(queryc, join_list[0] + join_list[1] + join_list[2] + join_list[3] + join_list[4] + join_list[5] + join_list[6] + join_list[7] + join_list[8] + join_list[9])
    toc = time()
    ot = toc-tic

    #To print the query output
    #for row in crsr.fetchall():
    #    print (row)
    print("Execution time of our model: ",(toc - tic))

    #List for cities
    join_list1 = sel_func_city(city, thresh,1)
    expected_output = ['victoria', 'vancouver', 'ottawa', 'toronto'] # take it from user
    #Calling the function
    check_accuracy(join_list1,expected_output)

    tick = time()
    #Query for city
    crsr.execute("SELECT b.NAME, a.post, a.city FROM  normal_post_city a INNER JOIN normal_name_post_city b ON a.city = b.city where a.city IN ('victoria', 'vancouver', 'ottawa', 'toronto')")

    tock = time()
    ora = tock-tick
    
    #To print the query output
    #for row in crsr.fetchall():
    #    print (row) 
    print("Regular Approach Execution time: ",(toc - tic))
    t = ot - ora
    print("Execution time difference between our approach and regular approach: ",t)
    

else:
    post = input("Enter the post name:") # developer
    thresh = int(input("Enter the threshold between 0-1:"))
    join_list = sel_func_post(post, thresh,0)
    queryp = join_table_fun_post(join_list)
    tic = time()
    #Query for post
    crsr.execute(queryp, join_list[0] + join_list[1] + join_list[2] + join_list[3] + join_list[4] + join_list[5] + join_list[6] + join_list[7] + join_list[8] + join_list[9])
    toc = time()
    ot = toc-tic

     #To print the query output
    #for row in crsr.fetchall():
    #    print (row)
    print("Execution time of our model: ",(toc - tic))

    #List for posts
    join_list1 = sel_func_post(post,thresh,1)
    expected_output = ['engineer', 'developer'] # take it from user
    #Calling the function
    check_accuracy(join_list1,expected_output)

    tick = time()
    #Change the expected ouput list with the IN parameters in the query

    #Query for post
    crsr.execute("SELECT b.NAME, a.post, a.city FROM  normal_post_city a INNER JOIN normal_name_post_city b ON a.post = b.post where a.post IN ('engineer','developer')")

    tock = time()
    ora = tock-tick

    #To print the query output
    #for row in crsr.fetchall():
    #    print (row) 
    print("Regular Approach Execution time: ",(toc - tic))
    t = ot - ora
    print("Execution time difference between our approach and regular approach: ",t)



# #Calculating execution time for regular query
# #Getting the execution time
# tick = time()
# #Change the expected ouput list with the IN parameters in the query

# #Query for post
# #crsr.execute("SELECT b.NAME, a.post, a.city FROM  normal_post_city a INNER JOIN normal_name_post_city b ON a.post = b.post where a.post IN ('engineer','developer')")

# #Query for city
# crsr.execute("SELECT b.NAME, a.post, a.city FROM  normal_post_city a INNER JOIN normal_name_post_city b ON a.city = b.city where a.city IN ('victoria', 'vancouver', 'ottawa', 'toronto')")

# tock = time()
# ora = tock-tick

# #To print the query output
# #for row in crsr.fetchall():
# #    print (row) 
# print("Regular Approach Execution time: ",(toc - tic))
# t = ot - ora
# print("Execution time difference between our approach and regular approach: ",t)