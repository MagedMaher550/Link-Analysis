import numpy

#Number Of Documents
N = 5

#function to generate a random string
def randString():
    import random
    alpha , pages , res , links = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ " , "" , "" , ""
    for i in range(1,N):
        pages += str(i)
    for i in range(N):
        links += pages[int(random.random()*len(pages))]
    for i in range(int(random.random()*100+20)):
        res += alpha[int(random.random()*len(alpha))]
    return res , links

#Generating random strings and saving them in files 1,2 up to n
def generate():
    page_link = {}
    for i in range(1,N+1):
        myRandString = randString()
        saveString(myRandString[0] , str(i) + ".txt")
        page_link[i] = myRandString[1]
    # saveString(randString()[0] , "Q.txt")

    return page_link


#function to save a string in a flile, note that the file name must be between quotation marks and the file must be in the same folder
def saveString(s , fileName):
    f = open(fileName , 'w')
    f.write(s)
    f.close

#function to read a file, note that the file name must be between quotation marks and the file must be in the same folder
def readFileAsString(fileName):
    f = open(fileName , 'r')
    myString = f.readline()
    f.close
    return myString

#function to search for a specific key in a dictionary
def serachnKeyObject(dict , value):
    for i in range(len(dict.keys())):
        if list(dict.keys())[i] == value:
            return list(dict.keys())[i]

#function to measure the frequency of letters in a given string
def freqCounter(s):
    res = {} 
    s = s.replace('\n' , '')
    for keys in s: 
        res[keys] = (res.get(keys, 0) + 1)
    return res

#sorting dictionary keys alphabetically
def sortDic(Dic):
    sortedList , sortedDic = sorted(list(Dic.items())) , {}
    for i in range(len(sortedList)):
       sortedDic [sortedList[i][0]] = sortedList[i][1]
    Dic = sortedDic
    return Dic

#adding unexistant keys with values equal to zero
def addValuesToDic(Dic):
    queryKeys = sorted(list(freqCounter(readFileAsString("Q.txt")).keys()))
    for i in range(len(queryKeys)):
        if queryKeys[i] not in Dic:
            Dic[queryKeys[i]] = 0
    return sortDic(Dic)

#function to calculate the term frequency for the document
def tf_dict(s):
    import collections
    res = addValuesToDic(freqCounter(s))
    div = collections.Counter(s).most_common(1)[0][1]
    for i in res:
        res[i] /= div
    return res

#function to generate a dictionary that have the frequency of each term in the collecttion
def IDF_Dict():
    generalDic = {}
    for i in range(1,N+1):
        generalDic.update(freqCounter(readFileAsString(str(i) + ".txt")))
        IDF_dic = {}
        for i in (generalDic.keys()):
            IDF_dic[i] = 0
            for j in range(1,N+1):
                if i in list(readFileAsString(str(j) + ".txt")):
                    IDF_dic[i] = IDF_dic[i] + 1
        flag = ""
    for i in readFileAsString("Q.txt"):
        if i in IDF_dic and flag != i:
            IDF_dic[i] += 1
            flag = i
        if i not in IDF_dic and i != '\n':
            IDF_dic[i] = 1
            flag = i
    return IDF_dic


def TF_IDF(fileName):
    import math
    tf = sortDic(tf_dict(readFileAsString(fileName)))
    idf = sortDic(addValuesToDic(IDF_Dict()))
    tf_idf_dict = {}

    for i in tf:
        x = idf[serachnKeyObject(idf , i)] # number of times the term i appeared in the documents
        a1 = float(N+1) / float(x)
        tf_idf_dict[i] = tf[i] * math.log(a1 , 2)
    return tf_idf_dict

#function to calculate the similarity between two documents
def sim(file1 , file2):
    TF_IDF_File1 = TF_IDF(file1)
    TF_IDF_File2 = TF_IDF(file2)
    res = 0

    for i in TF_IDF_File1:
        for j in TF_IDF_File2:
            if i == j:
                res += TF_IDF_File1[i] * TF_IDF_File2[j]
                break
    return res

def cosSim(file1, file2):
    import math
    TF_IDF_File1 = TF_IDF(file1)
    TF_IDF_File2 = TF_IDF(file2)
    file1_W , file2_W = 0 , 0
    
    for i in TF_IDF_File1:
        file1_W += (TF_IDF_File1[i])**2
    for i in TF_IDF_File2:
        file2_W += (TF_IDF_File2[i])**2

    div = (file1_W * file2_W)**0.5
    return sim(file1,file2) / div

#function to sort documents according to similarity
def sortDocuments():
    similarityDic = {"1" : cosSim("1.txt" , "Q.txt")}
    for i in range(N-1):
        similarityDic [str(i+2)] = cosSim(str(i+2) + ".txt" , "Q.txt")
    return sorted(list(similarityDic.items()), key=lambda x: x[1], reverse=True)
    
def showRes():
    res = "cosSimilarity:-\n\n"
    for i in range(len(sortDocuments())):
        res += '\t' + str(sortDocuments()[i][0]) + ".txt : " + str(round(sortDocuments()[i][1]*100,4)) + "%" + "\n"
    return res


#Link Analysis Code 

#Function to construct the adjacency matrix
def adjMtrx():
    links = generate()
    mtx = []
    for i in links:
        for j in links[i]:
            myList = [int(w) for w in list(links[i])]
            link = [1 if myList.count(w+1) > 0 else 0 for w in range(N)]
        mtx.append(link)    
    return mtx

#Function to calculate the authorith and hub for documents
def calc_Auth_hub():
    mtrx = adjMtrx()
    mtrxT = numpy.transpose(mtrx)

    h = [1 for i in range(N)]
    a = [1 for i in range(N)]

    for i in range(20):
        a = numpy.dot(mtrxT,h)
        ac , hc = 0 , 0
        for i in range(len(a)):
            ac += a[i]**2
        ac = ac**0.5
        a = numpy.divide(a,ac)

        h = numpy.dot(mtrx,a)

        for i in range(len(h)):
            hc += h[i]**2
        hc = hc**0.5
        h = numpy.divide(h,hc)

    return a , h

calc_Auth_hub()

#Function to arrange documents according to the authority and hub
def sortAuthHub():
    authority , hub = {} , {}
    a , h = calc_Auth_hub()[0] , calc_Auth_hub()[1]

    for i in range(len(a)):
        authority[str(i+1)] = a[i]
    for i in range(len(h)):
        hub[str(i+1)] = h[i]

    return (sorted(authority.items(), key=lambda x: x[1], reverse=True),
            sorted(hub.items(), key=lambda x: x[1], reverse=True))

def showAllRes():
    authority = sortAuthHub()[0]
    hub = sortAuthHub()[1]
    res1 = showRes()
    res2 , res3 = "Authority:-\n\n" , "Hub:-\n\n"
    for i in authority:
        res2 += '\t' + str(i[0]) + ".txt" + " : " + str(round(i[1],4)) +'\n'

    for i in hub:
        res3 += '\t' + str(i[0]) + ".txt" + ' : ' + str(round(i[1],4)) + '\n'
    return res1,res2,res3
