#SUBMITTED BY KAUSTUBH GANER

import pandas as pd
from collections import defaultdict
from itertools import chain, combinations
import time
##DATA-PREPROCESSING
df = pd.read_csv("adult.data",names=["age","workclass","final weight","education","education-num","martial-status","occupation","relationship","race","sex","capital-gain","capital-loss","hours-per-week","native-country","income"])
df = df[["workclass","education","martial-status","occupation","relationship","race","sex","native-country","income"]]
df.to_csv("complete_cleaned_data.csv",index=False)

def fpg(file, min_sup, conf_threshold):
    start_time = time.time()
    list_of_itemsets, freq = read_file(file)

    minimum_support_count = len(list_of_itemsets) * min_sup
    fp_tree, freq_dict = create_frequency_table_and_tree(list_of_itemsets, freq, minimum_support_count)
    freq_items_list = []
    tree_mining(freq_dict, minimum_support_count, set(), freq_items_list)
    end_time = time.time()
    print("Time required to run create frequent itemsets using FP Growth Algorithm is  :")
    print(f"{end_time - start_time} seconds")
    print("Generating Association Rules based on confidence")
    association_rules = []
    for itemset in freq_items_list:
        subsets = chain.from_iterable(combinations(itemset, i) for i in range(1, len(itemset)))
        itemset_sup = 0
        for j in list_of_itemsets:
            if set(itemset).issubset(j):
                itemset_sup += 1

        for subset in subsets:
            subset_sup = 0
            for j in list_of_itemsets:
                if set(subset).issubset(j):
                    subset_sup+=1
            conf = itemset_sup/subset_sup
            if conf>conf_threshold:
                association_rules.append([set(subset),set(itemset)-set(subset),conf])

    print("Done")
    return freq_items_list, association_rules


def read_file(file):
    output_ = []
    freq = []
    with open (file) as f:
        for line in f:
            output_.append(line.replace("\n", "").split(","))
            freq.append(1)
    return output_[1:],freq[1:]

class Node:
    def __init__(self, name, freq, parent):
        self.name = name
        self.count = freq
        self.parent = parent
        self.children = {}
        self.next = None

    def increment(self, freq):
        self.count += freq
def create_freq_table(list_of_itemsets,frequency,min_support):
    freq_table = defaultdict(float)
    # Counting frequency and creating a frequency table
    for num, itemSet in enumerate(list_of_itemsets):
        for item in itemSet:
            freq_table[item] += frequency[num]
    # filtering the frequency table to remove itemsets whose support is less than minimum support threshold
    freq_table = dict((item, support) for item, support in freq_table.items() if support >= min_support)

    return freq_table
def create_frequency_table_and_tree(list_of_itemsets: object, frequency: object, min_support):
    """Creates a frequency table and a tree"""
    freq_table = create_freq_table(list_of_itemsets,frequency,min_support)
    #modifying frequency table to store parent node as well
    for item in freq_table:
        freq_table[item] = [freq_table[item], None]
    #Creating a tree
    fp_tree = Node('Null', 1, None)
    for num, itemset in enumerate(list_of_itemsets):
        itemset = [item for item in itemset if item in freq_table]
        itemset.sort(key=lambda item: freq_table[item][0], reverse=True)
        current_node = fp_tree
        for item in itemset:
            current_node = tree_update(item, current_node, freq_table, frequency[num])
    return fp_tree, freq_table

def tree_update(item, tree_node, freq_table, frequency):
    "If the item is already present, we increment its count if not, we create a new node of that item"
    if item in tree_node.children:
        tree_node.children[item].increment(frequency)
    else:
        new_node = Node(item, frequency, tree_node)
        tree_node.children[item] = new_node
        if (freq_table[item][1] == None):
            freq_table[item][1] = new_node
        else:
            current_node = freq_table[item][1]
            while current_node.next != None:
                current_node = current_node.next
            current_node.next = new_node

    return tree_node.children[item]

def tree_ascend(node, prefix_path):
    "Recursive function for ascending the tree"
    if node.parent != None:
        prefix_path.append(node.name)
        tree_ascend(node.parent, prefix_path)

def pf_path(base_path, freq_table):
    tree_node = freq_table[base_path][1]
    frequency,conditional_pattern = [],[]
    while tree_node != None:
        prefix_path = []
        tree_ascend(tree_node, prefix_path)
        if len(prefix_path) > 1:
            conditional_pattern.append(prefix_path[1:])
            frequency.append(tree_node.count)

        tree_node = tree_node.next
    return conditional_pattern, frequency

def tree_mining(freq_table, minimum_supp_count, prefix, list_of_frequent_items):
    """Mining the tree for patterns"""
    # Sorting all the items and creating a list(in ascending order)
    list_of_sorted_items = [item[0] for item in sorted(list(freq_table.items()), key=lambda x:x[1][0])]
    for item in list_of_sorted_items:
        new_freq_set = prefix.copy()
        new_freq_set.add(item)
        list_of_frequent_items.append(new_freq_set)
        conditional_pattern_base, frequency = pf_path(item, freq_table)
        conditional_tree, new_freq_table = create_frequency_table_and_tree(conditional_pattern_base, frequency, minimum_supp_count)
        if new_freq_table != None:
            # Recursive mining of the tree till we get a empty frequency table
            tree_mining(new_freq_table, minimum_supp_count,new_freq_set, list_of_frequent_items)




frequent_items,rules = fpg("complete_cleaned_data.csv",0.2,0.6)
print("number of frequent itemsets given by  algorithm are : ",len(frequent_items))
