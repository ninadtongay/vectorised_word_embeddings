import io
import numpy as np
def get_vector(given_word):
  Glove = {}
  with io.open('app/business_logic/pca_embed2.txt', encoding='utf8') as f:
  #f = open('/content/drive/My Drive/NLP_Data/pca_embed2.txt')

      #print("Loading Glove vectors.")
      for line in f:
          values = line.split()
          word = values[0]
          if word == given_word:
            coefs = np.asarray(values[1:], dtype='float32')
            given_word_vector = coefs
            break
  f.close()
  return given_word_vector