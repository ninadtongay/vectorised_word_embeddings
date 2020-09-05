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
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix

from app.business_logic.get_word_vector import get_vector
from app.business_logic.cosine_sim import cos_sim
from app.business_logic.generate_data import get_data
from app.business_logic.sel_fun import sel_func_post,sel_func_city
from app.business_logic.sql_join import join_table_fun_city,join_table_fun_post,join_table_city,join_table_post
from app.business_logic.accuracy import check_accuracy

def entrypoint(n1, n2, choice, city, post, thresh, expected_output_city, expected_output_post):
    print("Processing")

    #Getting Vectors for available posts
    connection = sqlite3.connect("position_city_database_with_embeddings.db", check_same_thread=False)
    crsr = connection.cursor()

    post_list = ['engineer','manager','developer','ceo','cto','coo','waiter']
    city_list = ['victoria','vancouver','delhi','pune','ottawa','toronto','mumbai']

    #Getting input size
    # n1 = int(input("Enter number of rows for table containing Name,Post and City: "))
    # n2 = int(input("Enter number of rows for table containing Post and City: "))

    get_data(int(n1),int(n2))
    print("Data processing done")

    # choice= (input("Please enter choice (City/Post):"))
    if choice == 'City':
        # city = input("Enter the city name:") # vancouver
        # thresh = int(input("Enter the threshold between 0-1:"))
        join_list = sel_func_city(city, thresh,0) # Getting locations which having similarity score of more than .85 with 'Victoria'
        queryc = join_table_fun_city(join_list)
    
        #Query for city
        tic = time()
        crsr.execute(queryc, join_list[0] + join_list[1] + join_list[2] + join_list[3] + join_list[4] + join_list[5] + join_list[6] + join_list[7] + join_list[8] + join_list[9])
        toc = time()
        ot = toc-tic

        #To print the query output
        #for row in crsr.fetchall():
        #    print (row)
        print("Execution time of our model: ",(toc - tic))

        #List for cities
        join_list1 = sel_func_city(city, thresh,1)
        # expected_output = ['victoria', 'vancouver', 'ottawa', 'toronto'] # take it from user

        #Calling the function
        #check_accuracy(join_list1,expected_output_city)

        #Calculating Accuracy
        intersection = set(expected_output_city).intersection(set(join_list1))
        list_similarity = list(intersection)

        difference = set(expected_output_city).symmetric_difference(set(join_list1))
        list_difference = list(difference)

        if (len(list_difference)+len(expected_output_city))!=0:
            accuracy = len(list_similarity)/(len(list_difference)+len(expected_output_city))
        else:
            accuracy =1

        #Calculating Precision
        diff = set(city_list).symmetric_difference(set(expected_output_city))
        list_diff = list(diff)

        inter_correct = set(join_list1).intersection(set(list_diff))
        list_inter_correct = list(inter_correct)

        inter_false = set(list_diff).difference(set(join_list1))
        list_inter_false = list(inter_correct)

        if (len(list_similarity)+len(list_inter_correct))!=0:
            precision = len(list_similarity)/(len(list_similarity)+len(list_inter_correct))
        else:
            precision =1
        #Calculating Recall
        if (len(list_similarity)+len(list_inter_false))!=0:
            recall = len(list_similarity)/(len(list_similarity)+len(list_inter_false))
        else:
            recall =1
        #Calculating F1 Score
        F1 = 2 * (precision * recall) / (precision + recall)   
        
        queryci = join_table_city(expected_output_city)
        #Query for city
        tick = time()
        crsr.execute(queryci, expected_output_city)
        # crsr.execute("SELECT b.NAME, a.post, a.city FROM  normal_post_city a INNER JOIN normal_name_post_city b ON a.city = b.city where a.city IN ('victoria', 'vancouver', 'ottawa', 'toronto')")
        tock = time()
        ora = tock-tick
        
        #To print the query output
        #for row in crsr.fetchall():
        #    print (row) 
        print("Regular Approach Execution time: ",ora)
        t = ot - ora
        print("Execution time difference between our approach and regular approach: ",t)
        response = {
            "model_execution_time": ot,
            "regular_execution_time": ora,
            "time-difference": t,
            'accuracy': accuracy,
            'f1_score':F1
        }
        connection.close()
        return response

    else:
        # post = input("Enter the post name:") # developer
        # thresh = int(input("Enter the threshold between 0-1:"))
        join_list = sel_func_post(post, thresh,0)
        queryp = join_table_fun_post(join_list)
        #Query for post
        tic = time()        
        crsr.execute(queryp, join_list[0] + join_list[1] + join_list[2] + join_list[3] + join_list[4] + join_list[5] + join_list[6] + join_list[7] + join_list[8] + join_list[9])
        toc = time()
        ot = toc-tic

        #To print the query output
        #for row in crsr.fetchall():
        #    print (row)
        print("Execution time of our model: ",(toc - tic))

        #List for posts
        join_list1 = sel_func_post(post,thresh,1)
        # expected_output = ['engineer', 'developer'] # take it from user

        #Calling the function
        #check_accuracy(join_list1,expected_output_post)

        #Calculating Accuracy
        intersection = set(expected_output_post).intersection(set(join_list1))
        list_similarity = list(intersection)

        difference = set(expected_output_post).symmetric_difference(set(join_list1))
        list_difference = list(difference)

        if (len(list_difference)+len(expected_output_post))!=0:
            accuracy = len(list_similarity)/(len(list_difference)+len(expected_output_post))
        else:
            accuracy =1

        #Calculating Precision
        diff = set(post_list).symmetric_difference(set(expected_output_post))
        list_diff = list(diff)

        inter_correct = set(join_list1).intersection(set(list_diff))
        list_inter_correct = list(inter_correct)

        if len(list_difference)!=0:
            precision = len(list_inter_correct)/len(list_difference)
        else:
            precision =1

        #Calculating Recall
        if len(list_diff) and len(list_inter_correct)!=0:
            recall = len(list_inter_correct)/len(list_diff) 
        else:
            recall =1

        #Calculating F1 Score
        F1 = 2 * (precision * recall) / (precision + recall)   

        querypo = join_table_post(expected_output_post)
        #Query for post
        tick = time()
        crsr.execute(querypo, expected_output_post)
        # crsr.execute("SELECT b.NAME, a.post, a.city FROM  normal_post_city a INNER JOIN normal_name_post_city b ON a.post = b.post where a.post IN ('engineer','developer')")
        tock = time()
        ora = tock-tick

        #To print the query output
        #for row in crsr.fetchall():
        #    print (row) 

        print("Regular Approach Execution time: ",ora)
        t = ot - ora
        print("Execution time difference between our approach and regular approach: ",t)
        print("Accuracy:",accuracy)
        response = {
            "model_execution_time": ot,
            "regular_execution_time": ora,
            "time-difference": t,
            'accuracy': accuracy,
            'f1_score':F1
        }
        connection.close()
        return response

#Accuracy
#SQL Query updaetion
#Copmare flask and colab
