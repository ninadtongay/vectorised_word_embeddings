import numpy as np
import pandas as pd
import sqlite3

connection = sqlite3.connect("position_city_database_with_embeddings.db") 
crsr = connection.cursor() 


def sel_func_post(q,threshold):
  crsr.execute("select pi1,pi2,pi3,pi4,pi5,pi6,pi7,pi8,pi9,pi10 from em_post_name where post ='%s'" %q)
  q_vect = crsr.fetchall()
  crsr.execute("select pi1,pi2,pi3,pi4,pi5,pi6,pi7,pi8,pi9,pi10,post from em_post_name")
  t_vect = crsr.fetchall()
  vect_t = [tuple(list(x)[0:10]) for x in t_vect] # Getting all vectors in em_post_name
  vect_names = [list(x).pop(-1) for x in t_vect] # Getting all the corresponding post names to the vectors
  #print(vect_t) # Used to print all vectors in em_post_name
  #print(vect_names) # Used to print all the corresponding posts to the vectors
  similarity_array = [cos_sim(q_vect, x)[0] for x in vect_t] # Getting similarity scores for all vectors in table
  #print(similarity_array) # Used to print similary between vectors
  a = np.array(similarity_array)
  index = np.where(a > threshold)[0] # Getting index of all the post which are having similar value > threshold
  #print(index) # Printing indexes 
  new_vect_t = [vect_t[x] for x in index] # Getting new vectors according to those indexes
  #print(new_vect_t) # Printing the new vector
  #print(list(np.array(vect_t)[index][0])) # Checking the element
  join_list = []
  for x in range(0,len(new_vect_t[0])):
    join_list.append(tuple([i[x] for i in new_vect_t])) # Joining the new vectors together in a list
  #print(join_list) # To print the join_list
  return join_list # Returning the join_list


def sel_func_city(q,threshold):
  crsr.execute("select ci1,ci2,ci3,ci4,ci5,ci6,ci7,ci8,ci9,ci10 from em_city_name where city ='%s'" %q)
  q_vect = crsr.fetchall()
  crsr.execute("select ci1,ci2,ci3,ci4,ci5,ci6,ci7,ci8,ci9,ci10,city from em_city_name")
  t_vect = crsr.fetchall()
  vect_t = [tuple(list(x)[0:10]) for x in t_vect] # Getting all vectors in em_city_name
  vect_names = [list(x).pop(-1) for x in t_vect] # Getting all the corresponding city names to the vectors
  #print(vect_t) # Used to print all vectors in em_post_name
  #print(vect_names) # Used to print all the corresponding posts to the vectors
  similarity_array = [cos_sim(q_vect, x)[0] for x in vect_t] # Getting similarity scores for all vectors in table
  #print(similarity_array) # Used to print similary between vectors
  a = np.array(similarity_array) 
  index = np.where(a > threshold)[0] # Getting index of all the post which are having similar value > threshold
  #print(index) # Printing indexes 
  new_vect_t = [vect_t[x] for x in index] # Getting new vectors according to those indexes
  #print(new_vect_t) # Printing the new vector
  #print(list(np.array(vect_t)[index][0])) # Checking the element
  join_list = []
  for x in range(0,len(new_vect_t[0])):
    join_list.append(tuple([i[x] for i in new_vect_t]))  # Joining the new vectors together in a list
  #print(join_list) # To print the join_list
  return join_list # Returning the join_list

