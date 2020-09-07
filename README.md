


# Vectorised Word Embeddings - Unique way of involving NLP into DB
<p align="center">
  <img src="https://img.shields.io/github/last-commit/ninadtongay/vectorised_word_embeddings?style=flat-square"
         alt="GitHub last commit">
  <a href="https://github.com/navendu-pottekkat/nsfw-filter/issues">
  <img src="https://img.shields.io/github/issues/ninadtongay/vectorised_word_embeddings?style=flat-square&color=red"
         alt="GitHub issues">
  <a href="https://github.com/navendu-pottekkat/nsfw-filter/pulls">
  <img src="https://img.shields.io/github/issues-pr/ninadtongay/vectorised_word_embeddings?style=flat-square&color=blue"
         alt="GitHub pull requests">
  <img alt="Contributors" src="https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square" href="#contributors-">
  
------------------------------------
### Table of contents

- [Introduction](#introduction)
- [Research Problem Statement](#research-problem-statement)
- [Objectives](#objectives)
- [Versions](#versions)
- [Table Description](#table-description)
- [Installation](#installation)
    - [Python Flask](#python-flask)
    - [Google Colab](#google-colab)
- [Usage](#usage)
  - [Python Files](#python-files)
  - [Jupyter Notebook](#jupyter-notebook)
- [Result](#result)
- [Future Scope](#future-scope)
- [Contributors ✨](#contributors-)
- [License](#license)
------------------------------------
### Introduction
<a name="introduction" ></a>

This research is aimed towards understanding how NLP and DB concepts can be used together for awesomeness. The repository consists of methods for assessing string similarity based on word embedding representation using short embeddings rather than foreign keys or string fields to represent the join fields. We have implemented a join method based on the embedding similarity metrics and compared the results qualitatively with the current approach.

------------------------------------
### Research Problem Statement
<a name="problem-statement" ></a>

Consider a database in which one table T1 contains people and the city in which they live and table T2 contains job adverts and their location. We would like to pose a query that matches people and jobs based on a common location (a _string similarity join_). There are two ways to do this:

 1) To have a third table T3 that stores locations and then use a foreign key in T1 and T2 to refer to T3. We can then match people and jobs based on whether they reference the same foreign key id.
 2) To store the `city` and `location` as string fields and then compare them either based on string equality or a pattern matching expression.
Both of these approach are referred as Current/Regular approach ahead.

There are a host of problems with both approaches, however. The most obvious is that job locations may not be cities: they could be suburbs or states or countries or "remote"; so, an exact match won't work, neither for foreign key ids nor for string fields. This type of query can only really be supported with an extreme amount of data modelling on the part of an analyst.

Research in NLP have leapt decades ahead of this in terms of representing text and identifying similarity based on both semantics and syntax. If these NLP concepts were integrated directly into the database, one could answer a query like this effectively without requiring an analyst to sanitise all the data by hand. In this project, that is exactly what we have achieved.

------------------------------------
### Objectives


1. A framework to generate dummy data for testing purposes which would include:
a. Using <a href="https://nlp.stanford.edu/pubs/glove.pdf">Glove</a> pre-trained word.
b. Reducing the word vector dimensions(to 10 dimensions) using PCA.
c. Converting city names to word embeddings and storing them in the database.
d. Generating 6 tables, which will allow us to compare both the traditional and our research-based approach.
2. Implementing cosine similarity function
3. Methods for calculating cosine similarity on SQL table for `Job Posts` and `Cities`.
4. Methods to join two tables based on `Posts` or `Cities` using both approaches.
5. A framework to evaluate:
a. Accuracy.
b. Execution time.
c. F1 Score.
d. The difference in execution time between both approaches.

*Detailed description of code is provided in `NLP_Database_Fusion_Single_Words.ipynb` as comments* 

------------------------------------
### Table Description

1. Table1: Consists of persons name, embeddings of post, and embeddings of city.
![Table 1](/images/table1.png)
2. Normal Table1: Consists of  name, post, and city.
![Normal Table 1](/images/ntable1.png)
3. Table2: Consists of embeddings of post and embeddings of city.
![Table 2](/images/table2.png)
4. Normal Table2: Consists of post and city.
![Normal Table 2](/images/ntable2.png)
5. Table3: Consists of embeddings of post and name of posts.
![Table 3](/images/table3.png)
6. Table4: Consists of embeddings of city and name of cities.
![Table 4](/images/table4.png)

------------------------------------
### Versions
1. `Approach 1` : In this version we will measure the time required to execute the join query, without any overhead to improve the readability of the output (*Good for research purpose*). This approach is provided with both Google Colab / Jupyter Notebook and Python Flask App.
2. `Approach 2`: This is similar to approach 1, but this has additional overhead which helps in readibility of the output. This approach is provided with Google Colab / Jupyter notebook.

------------------------------------

### Installation
*Installation for both approaches is similar*
This project can be installed using two different methods:
1. Using [Python Flask](#python-flask)
2. Using [Google Colab](#google-colab)

#### Python Flask
1. To execute this code on your machine using python flask, you should first install all the dependencies mentioned in requirements.txt file.
```
pip3 install -r requirements.txt
```
2. Enter the `source` directory and execute the code using
```
python3 run.py
```
Voila! The python flask code is now up and running.
*Select enter Role as `Admin`* 


#### Google Colab
1. To execute this code on Google Colab / Jupyter Notebook, open `NLP_Database_Fusion_Single_Words.ipynb` (file name will also be having `approach` mentioned, use the one best suited for your needs)on your environment.
2. Update the location(address) used to access the database, word embeddings, and CSV files according to your local machine.

------------------------------------

### Usage
#### Python Files
- `pca_algo.py`: Used to reduce the vector dimensions using Principal Component Analysis. We reduce vectors having 50 dimensions to 10 dimensions. Word vectors are taken from Glove pre-trained word embeddings (https://nlp.stanford.edu/projects/glove/)
- `get_word_vector.py`: Used to return vectors for given words.
- `cosine_sim.py`: Returns similarity score between two words, ranging from 0 - 1. Where 1 means exactly similar and 0 means completely different.
- `sel_fun.py`: Consists of two functions(for comparing city and post vectors respectively) which takes word and threshold as an input. And then return vectors whose similarity scores are greater than the provided threshold. 
- `generate_data.py`: Used to generate variable size test data and create the required tables. Two tables with post word embeddings and city word embeddings will remain same for all the newly generated variable sized data.
- `sql_join.py`: Consists of SQL queries to join two tables according to the word embeddings.
- `accuracy.py`: Used to check the accuracy obtained while getting similar words through the pre-trained model.
- `vecnlp.py`(*Only avaiable when using python flask approach*): Used to accept the size of the table, select either city/post to find cosine similarity accordingly, threshold and expected output. Once executed, it will provide model execution time, regular approach execution time, accuracy and F1 score.

While implementing python flask method, these files are present in `source/app/business logic` folder.

#### Jupyter Notebook
This notebook consists of all the above mentioned python files in sequence.

------------------------------------
### Result
This research is implemented using two approaches:
1. In this approach, we have kept the only the essential body required to evaluate method(This is `Approach 1`).
![Approach 1 Google Colab](/images/approach1.png)
a.Implemented same (`Approach 1`) with a UI, built using Python Flask.
![a. Approach 2 Python Flask](/images/approach1a.png)
![b. Approach 2 Python Flask](/images/approach1b.png)
3. In this approach, we have added extra computations for better readability (displaying city names and posts after joining the tables), these computations act as overhead and reduce efficiency of our code(This is `Approach 2`).
![Approach 2 Google Colab](/images/approach2.png)
We compare both of the above approaches with the traditional method of joining SQL tables and the results were quite amazing.
![Regular Approach](/images/Regular_Approach.png)

The ratio of time difference between `Approach 1` to `Approach 2` approximately is : 3.67 (which changes according to the database and required output)

Following image shows the time difference between various data sample in all the mentioned approaches.
![Time difference](/images/td.png)
*Data size refers to number of rows*
*Time is measured in seconds*

------------------------------------

### Future Scope
- Improving Framework for evaluating SQL queries.
- Implementing words with space in between them(New York, New Delhi, etc)
- Training our own model for word embeddings.

------------------------------------

### Contributors ✨
Thanks go to Dr.Sean Chester who mentored me throughout this project and guided through it, without which this would not have been possible. :

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
      <td align="center"><a href=""><img src="https://avatars1.githubusercontent.com/u/18030768?s=460&u=99987bdaac58d0df47e02f14f953d497cc1abd50&v=4" width="100px;" alt=""/><br /><sub><b>Ninad Tongay</b></sub></a><br/></td>
    <td align="center"><a href="https://github.com/sean-chester"><img src="https://avatars0.githubusercontent.com/u/13118171?s=400&u=c410ad840806ccaadad50a4b65c87f3048c6f145&v=4" width="100px;" alt=""/><br /><sub><b>Dr. Sean Chester</b></sub></a><br /></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

Contributions are always welcome!
