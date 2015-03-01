'''
    Assigment 2
        This is an implementation of A-Priori algorithm to find frequent item sets
        Usage:
            python wenqiang_wang_apriori.py [INPUT FILE] [MINIMUM SUPPORT]
        Output:
            Frequent Itemsets of size A
            item1, item2, ..., itemA

            Frequent Itemsets of size B
            item1, item2, ..., itemB

            ...
'''
import sys

def tokenize(text):
    return text.strip().split(',')

def set_join(set1, set2):
    return list(set(set1).union(set(set2)))

def get_key(candidate):
    if type(candidate) == type(list()):
        candidate.sort()
        return ','.join(candidate)
    else:
        return candidate

def key2set(key):
    if ',' in key:
        return key.split(',')
    else:
        return [key]

def get_small_subset(c):
    #generate all (k-1)-size subsets of set c(list)
    subset = list()
    tmp = list()
    for i in range(0, len(c)):
        tmp = c.copy()
        del tmp[i]
        subset.append(tmp)
    return subset

def prune(candidate_set, freq_item):
    hash_table = dict()
    for item in freq_item:
        hash_table[get_key(item)] = True
    pruned_candidate_set = list()
    for s in candidate_set:
        flag = True
        ksubset = get_small_subset(s)
        for ss in ksubset:
            if get_key(ss) not in hash_table:
                flag = False
                break
        if flag:
            pruned_candidate_set.append(s)
    return pruned_candidate_set

def remove_duplicate(s):
    hash_table = dict()
    for elem in s:
        hash_table[get_key(elem)] = False
    i = len(s) - 1
    while i>=0:
        if hash_table[get_key(s[i])] == False:
            hash_table[get_key(s[i])] = True
        else:
            del s[i]
        i-=1
    return s

def generate_candidate_set(freq_item, k):
    candidate_set = list()

    for i in range(0, len(freq_item)-1):
        for j in range(i+1, len(freq_item)):
            new_candidate = set_join(freq_item[i], freq_item[j])
            if len(new_candidate) == k:
                candidate_set.append(new_candidate)
    candidate_set = remove_duplicate(candidate_set)
    if k>2:
        candidate_set = prune(candidate_set, freq_item)

    return candidate_set

def find_freq_item(log_path, candidate_set, k, support):
    handler = open(log_path)
    freq_count = dict()

    if len(candidate_set)>0:
        for candidate in candidate_set:
            freq_count[get_key(candidate)] = 0

    for line in handler:
        items = tokenize(line)
        items.sort()
        if len(candidate_set)>0:
            hash_item_list = dict()
            for it in items:
                hash_item_list[it] = True
            for candidate in candidate_set:
                is_in = True
                for it in candidate:
                    if it not in hash_item_list:
                        is_in = False
                        break
                if is_in:
                    freq_count[get_key(candidate)]+=1
        else:
            for it in items:
                if it not in freq_count:
                    freq_count[it] = 0
                freq_count[it]+=1
    handler.close()

    freq_set = list()
    for key in freq_count:
        if freq_count[key] >= support:
            freq_set.append(key2set(key))
    return freq_set

def main():
    if len(sys.argv)!=3:
        print('python '+sys.argv[0]+' [INPUT FILE] [MINIMUM SUPPORT]', file = sys.stderr)
        return
    input_path = sys.argv[1]
    min_support = int(sys.argv[2])
    handler = open('output.txt', 'w')
    candidate_set = list()

    k = 1

    while k == 1 or len(candidate_set)!=0:
        frequent_set = find_freq_item(input_path, candidate_set, k, min_support)
        if len(frequent_set)>0:
            handler.write('Frequent Itemsets of size '+str(k)+'\n')
        for i in range(0, len(frequent_set)):
            if len(frequent_set[i])>1:
                handler.write(','.join(frequent_set[i])+'\n')
            else:
                handler.write(frequent_set[i][0]+'\n')
        handler.write('\n')
        k+=1
        candidate_set = generate_candidate_set(frequent_set, k)

    handler.close()

if __name__ == '__main__':
    main()
