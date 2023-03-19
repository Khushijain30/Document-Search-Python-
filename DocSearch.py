import math

def dotProd(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))

def L(v):
    return math.sqrt(dotProd(v, v))

def angle(v1, v2):
    return (180/math.pi)*math.acos(dotProd(v1, v2) / (L(v1) * L(v2)))

with open("docs.txt", "r") as f:
    docs = []
    for line in f.readlines():
        line = line.strip()
        lineModified = line.maketrans("\t", " ")
        docs.append(line.translate(lineModified))

vocab = []
invertedIndex = {}
for id, doc in enumerate(docs):
    for word in doc.split(" "):
        if word not in vocab:
            vocab.append(word)
            invertedIndex[word] = [id+1]
        else:
            if (id+1) not in invertedIndex[word]:
                invertedIndex[word].append(id+1)

docVector = [[0 for i in range(len(vocab))] for j in range(len(docs))]
for id, doc in enumerate(docs):
    for word in doc.split(" "):
        docVector[id][vocab.index(word)] += 1

print("Words in dictionary: ",len(vocab))
with open("queries.txt", "r") as f:
    for line in f.readlines():
        query = line.strip()
        print("Query: ", query)
        relevantDocuments = []
        queryVector = [0 for i in range(len(vocab))]
        for word in query.split(" "):
            if word in invertedIndex:
                queryVector[vocab.index(word)] = 1
                relevantDocuments.append(invertedIndex[word])
        result = list(set.intersection(*map(set,relevantDocuments)))
        print("Relevant documents:", " ".join(str(x) for x in result))
        if len(result)!=0:
            search = []
            for docId in result:
                search.append((docId, angle(docVector[docId-1], queryVector)))
            sortedSearch = sorted(search, key=lambda x: x[1])
            for docId, angleVectors in sortedSearch:
                print("{0:d} {1:.2f}".format(docId, angleVectors))
