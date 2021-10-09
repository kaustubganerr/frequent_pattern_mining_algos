#SUBMITTED BY KAUSTUBH GANER

import time
from itertools import combinations
import pandas as pd
##DATA-PREPROCESSING
df = pd.read_csv("adult.data",names=["age","workclass","final weight","education","education-num","martial-status","occupation","relationship","race","sex","capital-gain","capital-loss","hours-per-week","native-country","income"])
df = df[["workclass","education","martial-status","occupation","relationship","race","sex","native-country","income"]]
df.to_csv("complete_cleaned_data.csv",index=False)
df_sample = df.sample(n = int(len(df)/3))
df_sample.to_csv("partial_data.csv",index=False)

## ALGORITHM
def apriori_(file,min_support_thresh):
    frequent_items = {}
    data = read_file(file)
    min_support_count = int(min_support_thresh*len(data))
    scan_1 = single_items_freq_table(data)
    l_1 = create_l_set(scan_1,min_support_count)
    for key,val in l_1.items():
        frequent_items[key] = val
    k =2
    sorted_dict = l_1
    while len(sorted_dict) != 0:
        c_set = create_c_set(sorted_dict,k=k)
        k+=1
        sorted_dict = get_count_and_prune(data,c_set,min_support_count)
        for key,val in sorted_dict.items():
            frequent_items[key] = val

    return frequent_items

def read_file(file):
    output_ = []
    with open (file) as f:
        for line in f:
            output_.append(line.replace("\n", "").split(","))
    return output_[1:]



def single_items_freq_table(data):
    first_scan = {}
    for item in data:
        for sub_item in item:
            if sub_item in first_scan.keys():
                first_scan[sub_item] += 1
            else:
                first_scan[sub_item]=1
    sorted_first_scan = dict(sorted(first_scan.items(),key = lambda x:x[1],reverse=True))
    return sorted_first_scan

def create_l_set(freq_table,min_support_count):
    above_threshold = dict((item, support) for item, support in freq_table.items() if support >= min_support_count)
    return above_threshold

def create_c_set(l_set,k):
    list_ = []
    if k ==2:
        for item_set in l_set:
            list_.append(item_set)
        create_sets_of_k = list(combinations(list_, k))
    elif k>2:
        for item_set in l_set:
            for item in item_set:
                list_.append(item)
                list_set = set(list_)

        create_sets_of_k = list(combinations(list_set, k))


    return create_sets_of_k
def get_count_and_prune(data,sets_of_k,min_support_count):
    count_dict = {}
    for i in sets_of_k:
        support_count = 0
        count_dict[i] = 0
        for itemset in data:
            if set(i).issubset(set(itemset)):
                count_dict[i] +=1
    prunned_dict = dict(sorted((key,value) for key,value in count_dict.items() if value > min_support_count ))
    sorted_dict = dict(sorted(prunned_dict.items(),key=lambda x : x[1],reverse=True))

    return sorted_dict




start = time.time()
frequent_items = apriori_("complete_cleaned_data.csv",0.2)
end = time.time()
print(f"Time Required to run Apriori on complete data, i.e original algorithm is : {end-start} seconds")
print("number of frequent items given by original algorithm are : ",len(frequent_items))
"""
MODIFICATION: RANDOM SAMPLING
INSTEAD OF RUNNING THE ALGORITHM ON ENTIRE DATA, WE WILL RANDOMLY SELECT 1/3 DATA POINTS
AND RUN APRIORI ON THEM AND COMPARE THE RESULTS
"""
start = time.time()
partial_frequent_times = apriori_("partial_data.csv",0.2)
end = time.time()
print(f"Time Required to run Apriori on partial data, i.e modified  algorithm is : {end-start} seconds")
print("number of frequent items given by modified algorithm are : ",len(partial_frequent_times))

