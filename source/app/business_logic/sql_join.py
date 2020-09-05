import sqlite3
from itertools import repeat

connection = sqlite3.connect("position_city_database_with_embeddings.db", check_same_thread=False) 
crsr = connection.cursor() 
def makeqmarks(i):
    return ', '.join(repeat('?', i))

#placeholder = '?'
#format_strings = ','.join(['%s'] * len(join_list[0]))


def join_table_fun_city(join_list):

# ************* Join table query *************
  queryc = 'SELECT b.NAME \
  FROM post_city a \
  INNER JOIN name_post_city b \
  ON a.ci1 = b.ci1 AND \
  a.ci2 = b.ci2 AND \
  a.ci3 = b.ci3 AND \
  a.ci4 = b.ci4 AND \
  a.ci5 = b.ci5 AND \
  a.ci6 = b.ci6 AND \
  a.ci7 = b.ci7 AND \
  a.ci8 = b.ci8 AND \
  a.ci9 = b.ci9 AND \
  a.ci10 = b.ci10 \
  WHERE \
  a.ci1 IN (%s) AND \
  a.ci2 IN (%s) AND \
  a.ci3 IN (%s) AND \
  a.ci4 IN (%s) AND \
  a.ci5 IN (%s) AND \
  a.ci6 IN (%s) AND \
  a.ci7 IN (%s) AND \
  a.ci8 IN (%s) AND \
  a.ci9 IN (%s) AND \
  a.ci10 IN (%s);' \
  % (makeqmarks(len(join_list[0])), makeqmarks(len(join_list[1])), makeqmarks(len(join_list[2])),makeqmarks(len(join_list[3])),makeqmarks(len(join_list[4])),makeqmarks(len(join_list[5])),makeqmarks(len(join_list[6])),makeqmarks(len(join_list[7])),makeqmarks(len(join_list[8])),makeqmarks(len(join_list[9])))
  #print(join_list[0]) # To check the elements in 0th index
  return queryc

def join_table_fun_post(join_list):

# ************* Join table query *************
  queryp = 'SELECT b.NAME \
  FROM post_city a \
  INNER JOIN name_post_city b \
  ON a.ci1 = b.ci1 AND \
  a.pi2 = b.pi2 AND \
  a.pi3 = b.pi3 AND \
  a.pi4 = b.pi4 AND \
  a.pi5 = b.pi5 AND \
  a.pi6 = b.pi6 AND \
  a.pi7 = b.pi7 AND \
  a.pi8 = b.pi8 AND \
  a.pi9 = b.pi9 AND \
  a.pi10 = b.pi10 \
  WHERE \
  a.pi1 IN (%s) AND \
  a.pi2 IN (%s) AND \
  a.pi3 IN (%s) AND \
  a.pi4 IN (%s) AND \
  a.pi5 IN (%s) AND \
  a.pi6 IN (%s) AND \
  a.pi7 IN (%s) AND \
  a.pi8 IN (%s) AND \
  a.pi9 IN (%s) AND \
  a.pi10 IN (%s);' \
  % (makeqmarks(len(join_list[0])), makeqmarks(len(join_list[1])), makeqmarks(len(join_list[2])),makeqmarks(len(join_list[3])),makeqmarks(len(join_list[4])),makeqmarks(len(join_list[5])),makeqmarks(len(join_list[6])),makeqmarks(len(join_list[7])),makeqmarks(len(join_list[8])),makeqmarks(len(join_list[9])))
  #print(join_list[0]) # To check the elements in 0th index
  return queryp

def join_table_city(join_list):

# ************* Join table query *************
  queryc = 'SELECT b.NAME \
  FROM normal_post_city a \
  INNER JOIN normal_name_post_city b \
  ON a.city = b.city \
  WHERE \
  a.city IN (%s);' \
  % (makeqmarks(len(join_list)))
  #print(join_list[0]) # To check the elements in 0th index
  return queryc

def join_table_post(join_list):

# ************* Join table query *************
  queryp = 'SELECT b.NAME \
  FROM normal_post_city a \
  INNER JOIN normal_name_post_city b \
  ON a.post = b.post \
  WHERE \
  a.post IN (%s);' \
  % (makeqmarks(len(join_list)))
  #print(join_list[0]) # To check the elements in 0th index
  return queryp
