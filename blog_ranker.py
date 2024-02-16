import string
import io

def trigrams(textArray):
    trigram = []
    for i in range(len(textArray)-3+1):
        trigram.append(textArray[i:i+3])
    for i in range(len(textArray)-2+1):
        trigram.append(textArray[i:i+2])
    for i in range(len(textArray)):
        trigram.append(textArray[i])
    return trigram

def intersection(list1, list2):
	list3 = [value for value in list1 if value in list2]
	return list3
    
def jaccardSimilarity(s1Trigrams,s2Trigrams,s2TrigramIndex,s2len):

    s2Trigrams=s2Trigrams[:s2TrigramIndex] + s2Trigrams[s2TrigramIndex+s2len:]
    s1Trigrams = set(map(tuple, [ngram for ngram in s1Trigrams]))
    s2Trigrams = set(map(tuple, [ngram for ngram in s2Trigrams]))
    intersectionlen = len(s1Trigrams.intersection(s2Trigrams))
    unionlen = len(s1Trigrams.union(s2Trigrams))

    # intersectionlen = len(intersection(s2Trigrams,s1Trigrams))
    # unionlen = len(s2Trigrams)
    
    return (intersectionlen) /(unionlen)

def editDistance(s1,s2):

    distance = [[float("inf") for j in range(len(s2)+1)] for i in range(len(s1)+1)] 

    for i in range(len(s1) + 1):
        distance[i][len(s2)] = len(s1)-i

    for j in range(len(s2) + 1):
        distance[len(s1)][j] = len(s2)-j

    for i in range(len(s1)-1,-1,-1):
        for j in range(len(s2)-1,-1,-1):
            if s1[i] == s2[j]:
                distance[i][j]=distance[i+1][j+1]
            else:  
                distance[i][j] = 1+min(distance[i+1][j], distance[i][j+1], distance[i+1][j+1])
    
    return distance[0][0]

def similarity(s1, s2, s2Trigrams, exclude_index, exclude_len,s2TrigramIndex,s2len):
   
    s1Trigrams = trigrams(s1)

    jaccard = jaccardSimilarity(s1Trigrams,s2Trigrams,s2TrigramIndex,s2len)

    s2 = s2[:exclude_index] + s2[exclude_index+exclude_len:]

    editDistanceScore=(1-editDistance(s1,s2)/max(len(s1),len(s2)))

    # print(jaccard,editDistanceScore)
    alpha=0.5
    similarityScore = alpha*jaccard + (1-alpha)*editDistanceScore

    return similarityScore

blogNames=["t.txt","x.txt","t1.txt"]

allBlogsArray=[]
blogStartIndex=[]
s2TrigramStartIndex=[]
s2len=[]
textInBlogArray=[]
s2Trigrams=list()

for blog in blogNames:
    file=io.open(blog, mode="r", encoding="utf-8")
    textInBlog=file.read()
    textInBlog=textInBlog.lower()
    textInBlog = textInBlog.translate(str.maketrans('', '', string.punctuation))

    textArray = textInBlog.split()

    textInBlogArray.append(textArray)
    blogStartIndex.append(len(allBlogsArray))
    allBlogsArray+=textArray
    s2TrigramStartIndex.append(len(s2Trigrams))
    temtri=trigrams(textArray)
    s2Trigrams+=temtri
    s2len.append(len(temtri))

    file.close()

blogScores=[[0 for j in range(2)] for i in range(len(textInBlogArray))] 

for j,i in enumerate(textInBlogArray):
    similarityScore=similarity(i,allBlogsArray,s2Trigrams,blogStartIndex[j],len(i),s2TrigramStartIndex[j],s2len[j])
    blogScores[j][0]=blogNames[j]
    blogScores[j][1]=similarityScore

blogScores.sort(key = lambda x: x[1])

print(blogScores)