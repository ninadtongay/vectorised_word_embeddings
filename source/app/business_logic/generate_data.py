#!pip install faker
import pandas as pd
import sqlite3
import numpy as np
from itertools import repeat
from faker import Faker
from sklearn.utils import shuffle
#Generating Data
def get_data(n,j):
  #Getting fake names
  fake = Faker()
  name_df = [fake.name() for i in range(n)]
  name_df = pd.DataFrame((name_df),columns=['name'])

  #Dataframe with Vectors for respective posts and post
  data = pd.read_csv (r'app/business_logic/csv/table3_vectors_for_posts.csv')   
  orig_post_df = pd.DataFrame(data, columns= ['pi1','pi2','pi3','pi4','pi5','pi6','pi7','pi8','pi9','pi10','post'])
  post_df = orig_post_df.iloc[:,:]
  #print(df3)

  #Dataframe with Vectors for respective cities and city
  data = pd.read_csv (r'app/business_logic/csv/table4_vectors_for_cities.csv')
  orig_city_df = pd.DataFrame(data, columns= ['ci1','ci2','ci3','ci4','ci5','ci6','ci7','ci8','ci9','ci10','city'])
  city_df = orig_city_df.iloc[:,:]
  #print(df4)

    #Shuffling and storing the data n times
  new_city_df = city_df
  new_post_df = post_df

  for i in range(int(n/7)):
    city_df = shuffle(city_df)
    post_df = shuffle(post_df)
    new_city_df = pd.concat([new_city_df, city_df], axis=0)
    new_post_df = pd.concat([new_post_df, post_df], axis=0)

  #Getting n number of data
  normal_city_df = new_city_df.iloc[:,10]
  normal_post_df = new_post_df.iloc[:,10]
  n_city_df = new_city_df.iloc[:,:-1]
  n_post_df = new_post_df.iloc[:,:-1]

  n_city_df= new_city_df.head(n)
  n_post_df= new_post_df.head(n)
  normal_city_df= normal_city_df.head(n)
  normal_post_df= normal_post_df.head(n)

  #Resetting index
  n_city_df.reset_index(drop=True, inplace=True)
  n_post_df.reset_index(drop=True, inplace=True)
  normal_city_df.reset_index(drop=True, inplace=True)
  normal_post_df.reset_index(drop=True, inplace=True)

  #Dataframe ready for table 1 with name, post and city word embeddings
  df1 = pd.concat([name_df,n_post_df,n_city_df], axis=1)
  normal_df1 = pd.concat([name_df,normal_post_df,normal_city_df], axis=1)
  #print(df1)

  #Shuffling and resetting index for table 2 
  new_city_df = shuffle(new_city_df)
  new_post_df = shuffle(new_post_df)

  normal2_city_df = new_city_df.iloc[:,10]
  normal2_post_df = new_post_df.iloc[:,10]
  new_city_df = new_city_df.iloc[:,:-1]
  new_post_df = new_post_df.iloc[:,:-1]

  new_city_df= new_city_df.head(j)
  new_post_df= new_post_df.head(j)
  normal2_city_df= normal_city_df.head(j)
  normal2_post_df= normal_post_df.head(j)

  new_city_df.reset_index(drop=True, inplace=True)
  new_post_df.reset_index(drop=True, inplace=True)

  #Dataframe ready for table 2 with post and city
  df2 = pd.concat([new_post_df,new_city_df], axis=1)
  normal_df2 = pd.concat([normal2_post_df,normal2_city_df], axis=1)
  #print(df2)

  #Creating database
  connection = sqlite3.connect("position_city_database_with_embeddings.db", check_same_thread=False)
  crsr = connection.cursor() 

  #Comment the table creation and insertion of data into the table if the database is already created once.
  #Creating table1 with name, embeddings of post, and embeddings of city
  crsr.execute('CREATE TABLE name_post_city (NAME nvarchar(50),pi1 float,pi2 float,pi3 float,pi4 float,pi5 float,pi6 float,pi7 float,pi8 float,pi9 float,pi10 float, ci1 float,ci2 float,ci3 float,ci4 float,ci5 float,ci6 float,ci7 float,ci8 float,ci9 float,ci10 float, FOREIGN KEY (ci1,ci2,ci3,ci4,ci5,ci6,ci7,ci8,ci9,ci10) REFERENCES em_city_name(ci1,ci2,ci3,ci4,ci5,ci6,ci7,ci8,ci9,ci10), FOREIGN KEY (pi1,pi2,pi3,pi4,pi5,pi6,pi7,pi8,pi9,pi10) REFERENCES em_post_city(pi1,pi2,pi3,pi4,pi5,pi6,pi7,pi8,pi9,pi10))')
  df1.to_sql('name_post_city', connection, if_exists='replace', index = False)
  crsr.execute('''SELECT * FROM name_post_city''')
  # print("Table 1: Name_Post_City Data")
  # for row in crsr.fetchall():
  #     print (row)

  #Creating normal table1 with name,post, and city
  crsr.execute('CREATE TABLE normal_name_post_city (NAME nvarchar(50),pi1 float,pi2 float,pi3 float,pi4 float,pi5 float,pi6 float,pi7 float,pi8 float,pi9 float,pi10 float, ci1 float,ci2 float,ci3 float,ci4 float,ci5 float,ci6 float,ci7 float,ci8 float,ci9 float,ci10 float, FOREIGN KEY (ci1,ci2,ci3,ci4,ci5,ci6,ci7,ci8,ci9,ci10) REFERENCES em_city_name(ci1,ci2,ci3,ci4,ci5,ci6,ci7,ci8,ci9,ci10), FOREIGN KEY (pi1,pi2,pi3,pi4,pi5,pi6,pi7,pi8,pi9,pi10) REFERENCES em_post_city(pi1,pi2,pi3,pi4,pi5,pi6,pi7,pi8,pi9,pi10))')
  normal_df1.to_sql('normal_name_post_city', connection, if_exists='replace', index = False)
  crsr.execute('''SELECT * FROM normal_name_post_city''')
  # print("Normal Table 1: Normal_Name_Post_City Data")
  # for row in crsr.fetchall():
  #     print (row)

  #Creating table2 with embeddings of post and embeddings of city
  crsr.execute('CREATE TABLE post_city (pi1 float,pi2 float,pi3 float,pi4 float,pi5 float,pi6 float,pi7 float,pi8 float,pi9 float,pi10 float, ci1 float,ci2 float,ci3 float,ci4 float,ci5 float,ci6 float,ci7 float,ci8 float,ci9 float,ci10 float, FOREIGN KEY (ci1,ci2,ci3,ci4,ci5,ci6,ci7,ci8,ci9,ci10) REFERENCES em_city_name(ci1,ci2,ci3,ci4,ci5,ci6,ci7,ci8,ci9,ci10), FOREIGN KEY (pi1,pi2,pi3,pi4,pi5,pi6,pi7,pi8,pi9,pi10) REFERENCES em_post_city(pi1,pi2,pi3,pi4,pi5,pi6,pi7,pi8,pi9,pi10))')
  df2.to_sql('post_city', connection, if_exists='replace', index = False)
  # print("\nTable 2: Post_City Data")
  # crsr.execute('''SELECT * FROM post_city''')
  # for row in crsr.fetchall():
  #     print (row)
  

  #Creating normal table2 with post and city
  crsr.execute('CREATE TABLE normal_post_city (pi1 float,pi2 float,pi3 float,pi4 float,pi5 float,pi6 float,pi7 float,pi8 float,pi9 float,pi10 float, ci1 float,ci2 float,ci3 float,ci4 float,ci5 float,ci6 float,ci7 float,ci8 float,ci9 float,ci10 float, FOREIGN KEY (ci1,ci2,ci3,ci4,ci5,ci6,ci7,ci8,ci9,ci10) REFERENCES em_city_name(ci1,ci2,ci3,ci4,ci5,ci6,ci7,ci8,ci9,ci10), FOREIGN KEY (pi1,pi2,pi3,pi4,pi5,pi6,pi7,pi8,pi9,pi10) REFERENCES em_post_city(pi1,pi2,pi3,pi4,pi5,pi6,pi7,pi8,pi9,pi10))')
  normal_df2.to_sql('normal_post_city', connection, if_exists='replace', index = False)
  # print("\nNormal Table 2: Normal_Post_City Data")
  # crsr.execute('''SELECT * FROM normal_post_city''')
  # for row in crsr.fetchall():
  #     print (row)

  #Creating table3 with embeddings of post and name of posts
  crsr.execute('CREATE TABLE em_post_name (pi1 float,pi2 float,pi3 float,pi4 float,pi5 float,pi6 float,pi7 float,pi8 float,pi9 float,pi10 float, post nvarchar(50), PRIMARY KEY(pi1,pi2,pi3,pi4,pi5,pi6,pi7,pi8,pi9,pi10))')
  orig_post_df.to_sql('em_post_name', connection, if_exists='replace', index = False)
  # print("\nTable 3: Em_Post_Name Data")
  # crsr.execute('''SELECT * FROM em_post_name''')
  # for row in crsr.fetchall():
  #     print (row)

  #Creating table4 with embeddings of city and name of cities
  crsr.execute('CREATE TABLE em_city_name (ci1 float,ci2 float,ci3 float,ci4 float,ci5 float,ci6 float,ci7 float,ci8 float,ci9 float,ci10 float, city nvarchar(50), PRIMARY KEY(ci1,ci2,ci3,ci4,ci5,ci6,ci7,ci8,ci9,ci10))')
  orig_city_df.to_sql('em_city_name', connection, if_exists='replace', index = False)
  # print("\nTable 4: Em_City_Name Data")
  # crsr.execute('''SELECT * FROM em_city_name''')
  # for row in crsr.fetchall():
  #     print (row)

  connection.commit()

  #Execute the following line to print all the SQL queries when executed
  #connection.set_trace_callback(print)

  #Incase you want to drop all tables:
  #crsr.execute('DROP TABLE name_post_city')
  #crsr.execute('DROP TABLE post_city')
  #crsr.execute('DROP TABLE em_post_name')
  #crsr.execute('DROP TABLE em_city_name')
  #connection.commit()  

#get_data(10000,5000)