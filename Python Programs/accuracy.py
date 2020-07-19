#Checking the model
def check_accuracy(join_list, expected_output):
  if join_list == expected_output:
    a = (len(join_list) / len(expected_output))*100
    print("Accuracy =",a)
  else:
    difference = set(expected_output).symmetric_difference(set(join_list))
    list_difference = list(difference)
    #print(list_difference)
    intersection = set(expected_output).intersection(set(join_list))
    list_similarity = list(intersection)
    #print(list_similarity)
    out_off = len(list_difference) + len(list_similarity)
    #print(out_off)
    #print(list_similarity)
    a = (len(list_similarity) / out_off)*100
    print("Accuracy =",a,"%")