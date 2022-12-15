import numpy as np
import pandas as pd


# test data
def loadTestSet():
    return [['a', 'c', 'e'], ['b', 'd'], ['b', 'c'], ['a', 'b', 'c', 'd'], ['a', 'b'], ['b', 'c'], ['a', 'b'],
            ['a', 'b', 'c', 'e'], ['a', 'b', 'c'], ['a', 'c', 'e']]


def loadCattle():
    file_name = "../data/data_proced.csv"
    import csv
    ans = []
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            row = list(set(row))  # De-duplication and sorting
            row.sort()
            while '' in row:
                row.remove('')
            ans.append(row)
    return ans


def creatC1(data):
    """
    :param data: dataset
    :return: one candidate set C1
    """
    C1 = []
    for row in dataSet:
        for item in row:
            if [item] not in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))


def calSupport(D, C, minSupport):
    """
    :param D: dataset
    :param C1: Candidate set
    :param minSupport: Minimum Support
    :return: Return the 1-item frequent set and its support
    """
    dict_sup = {}
    for i in D:
        for j in C:
            if j.issubset(i):
                if j not in dict_sup:
                    dict_sup[j] = 1
                else:
                    dict_sup[j] += 1
    # Total number of transactions
    sumCount = float(len(D))
    # Calculate support, support = count of set of items/total number of transactions
    supportData = {}
    relist = []
    for i in dict_sup:
        temp_sup = dict_sup[i] / sumCount
        if temp_sup > minSupport:
            relist.append(i)
            supportData[i] = temp_sup
    return relist, supportData


def aprioriGen(Lk, k):
    """
    Using the pruning algorithm, the candidate set space is reduced and the k-item candidate set is found
    :param Lk: k-1 frequent sets
    :param k: kth
    :return: kth candidate set
    """
    reList = []  # Store the kth candidate set
    lenLk = len(Lk)  # Length of the k-1th frequent set
    # Two-by-two traversal
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                a = Lk[i] | Lk[j]
                # Performing pruning
                a1 = list(a)
                b = []

                for q in range(len(a1)):
                    t = [a1[q]]
                    tt = frozenset(set(a1) - set(t))
                    b.append(tt)

                # If b is a frequent set, keep a1, otherwise, delete
                t = 0
                for w in b:
                    if w in Lk:
                        t += 1
                if len(b) == t:
                    reList.append(b[0] | b[1])

    return reList


def scanD(D, Ck, minSupport):
    """
    Calculate the support of the candidate k-item set,
    eliminate the candidate set with less than the minimum support, and get the frequent k-item set and its support
    :param D: dataset
    :param Ck: Candidate k-item set
    :param minSupport: Minimum Support
    :return: Return the set of frequent k items and its support
    """
    sscnt = {}  # Storage support
    for tid in D:  # Traversing the data set
        for can in Ck:  # Iterate through the candidates
            if can.issubset(tid):  # Whether the dataset contains candidate items
                if can not in sscnt:
                    sscnt[can] = 1
                else:
                    sscnt[can] += 1

    # Calculating support
    numItem = len(D)  # Total number of transactions
    reList = []  # Store k-item frequent sets
    supportData = {}  # Store frequent set correspondence support
    for key in sscnt:
        support = sscnt[key] / numItem
        if support > minSupport:
            reList.insert(0, key)  # Add to Lk if conditions are met
            supportData[key] = support
    return reList, supportData


def apriori(dataSet, minSupport=0.2):
    """
    apriori algorithm
    :param data: data
    :param minSupport: Minimum Support
    :return: Return the frequent set and the corresponding support
    """
    C1 = creatC1(dataSet)
    D = list(map(set, dataSet))
    L1, supportData = calSupport(D, C1, minSupport)
    L = [L1]

    k = 2
    # If there is no candidate set then exit the loop
    while len(L[k - 2]) > 0:
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    del L[-1]
    return L, supportData


def getSubset(fromList, totalList):
    """
    Generate all subsets of a set
    :param fromList:
    :param totalList:
    """
    for i in range(len(fromList)):
        t = [fromList[i]]
        tt = frozenset(set(fromList) - set(t))

        if tt not in totalList:
            totalList.append(tt)
            tt = list(tt)
            if len(tt) > 1:
                getSubset(tt, totalList)


def calcConf(freqSet, H, supportData, ruleList, minConf):
    """
    Calculate the confidence level and eliminate data with less than
    the minimum confidence level, using the concept of lift here
    :param freqSet: k frequent sets
    :param H: All subsets corresponding to k frequent sets
    :param supportData: support
    :param RuleList: Minimum confidence
    :param minConf: Minimum confidence
    """
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]

        # lift=p(a&b)/p(a)*p(b)
        lift = supportData[freqSet] / (supportData[conseq] * supportData[freqSet - conseq])
        if conf >= minConf and lift > 1:
            print(freqSet - conseq, '-->', conseq, 'Support', round(supportData[freqSet], 6), 'Confidence：',
                  round(conf, 6),
                  'lift：', round(lift, 6))
            ruleList.append((freqSet - conseq, conseq, round(conf, 6), round(supportData[freqSet], 6), round(lift, 6)))


def get_rule(L, supportData, minConf=0.7):
    """
    Generate strong association rules: Strong association rules are
    generated when the minimum confidence threshold is met in the set of frequent items
    :param L: Frequent sets
    :param supportData: support
    :param minConf: Minimum confidence
    :return: Return to Strong Association Rules
    """
    bigRuleList = []  # Store strong association rules
    # Calculate confidence level from 2th frequent set
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = list(freqSet)
            all_subset = []
            getSubset(H1, all_subset)
            calcConf(freqSet, all_subset, supportData, bigRuleList, minConf)
    return bigRuleList


if __name__ == '__main__':
    # dataSet = loadTestSet()
    dataSet = loadCattle()
    L, supportData = apriori(dataSet, minSupport=0.25)
    rule = get_rule(L, supportData, minConf=0.1)
    name = ['Item1', 'Item2', 'Confidence', 'Support', 'Lift']
    rule_df = pd.DataFrame(columns=name, data=rule)
    # print(rule_df)
    rule_df.to_csv('../data/Rules.csv', encoding='gbk')
    print("Finish!")
