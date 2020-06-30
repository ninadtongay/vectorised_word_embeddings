Vectorised Word Embeddings
============

This repository consists of methods for assessing string similarity based on word embedding representation. Using short embeddings rather than foreign keys or string fields to represent the join fields. Implementing a join method based on the embedding similarity metrics and comparing the results qualitatively with the current approach.

---

## Table of Contents
- Python Files
- Jupyter Notebook
- Ongoing Work and Upcoming Features

---

## Python Files
- pca_algo.py: Used to reduce the vector dimensions using Principal Component Analysis. We reduce vectors having 50 dimensions to 10 dimensions. Word vectors are taken from Glove pre-trained word embeddings (https://nlp.stanford.edu/projects/glove/)
- get_word_vector.py: Used to return vectors for given words.
- cosine_sim.py: Returns similarity score between two words, ranging from 0 - 1. Where 1 means exactly similar and 0 means completely different.
- sel_fun.py: Consists of two functions(for comparing city and post vectors respectively) which takes word and threshold as an input. And then return vectors whose similarity scores are greater than the provided threshold. 

---

## Jupyter Notebook (NLP_Database_Fusion_Single_Words.ipynb)

This notebook consists of the code to create SQL database, use the python functions to carry out various operations, and SQL Query to join tables based on the similarity between word vectors.

---

## Ongoing Work and Upcoming Features
- Framework generation for evaluating SQL queries.
- A framework to enable data scaling.
- Comparing results with regular SQL approach.
