import sys, os, random, re, math

vocabSize = 0
Nx = 1.0

# -------------------------
# BEGIN PREPROCESSING PHASE
# -------------------------

class BayesFeature():
    def __init__(self, word, idx, features):
        global vocabSize, Nx
        self.ff = 0
        self.ft = 0
        self.tf = 0
        self.tt = 0
        self.clf = 0
        self.clt = 0
        for feature in features:
            if feature[-1] == 0:
                self.clf += 1
                if feature[idx] == 0:
                    self.ff += 1
                else:
                    self.tf += 1
            else:
                self.clt += 1
                if feature[idx] == 0:
                    self.ft += 1
                else:
                    self.tt += 1
        self.probabilities = [[float(float(self.ff + Nx)/(self.clf + vocabSize)),float(float(self.ft + Nx)/(self.clt + vocabSize))], [float(float(self.tf + Nx)/(self.clf + vocabSize)), float(float(self.tt + Nx)/(self.clt + vocabSize))]]

    def getProb(self, x, y):
        return self.probabilities[x][y]

    def clProb(self, x):
        if x:
            return float(self.clt) / (self.clt + self.clf)
        else:
            return float(self.clf) / (self.clt + self.clf)

class Vocabulary():
    def __init__(self):
        self.commonWords = []
        self._words = {}

    def put(self, word):
        if word in self._words:
            self._words[word] += 1
        else:
            self._words[word] = 1

    def get(self, word):
        if word in self._words:
            return self._words[word]
        else:
            return 0

    def contains(self, word):
        if word in self._words:
            return 1
        else:
            return 0

    def buildArray(self):
        global vocabSize
        for key, val in self._words.iteritems():
            if val > 5:
                self.commonWords.append(key)
        self.commonWords = sorted(self.commonWords)
        vocabSize = len(self.commonWords)

# Read each line of a file into a 2D array containing sentence and class label
# PARAMS: Name of the file to read. Must be in working directory.
# RETURN: 2d-Array containing sentence[0] and  classlabel[1]
def readRawFile(filename):
    sentences = []
    with open(filename) as f:
        content = f.readlines()
    for line in content:
        raw = re.findall('(".*?",)|(?<=,)([0-1])', line)
        sentences.append([raw[0][0].lower(), raw[1][1]])
    return sentences

# Remove all apostrophes from each sentence in an array of sentences.
# PARAMS: Array of strings to clean
# RETURN: Array of original strings minus apostrophes
def removeSymbols(sentences):
    for sentence in sentences:
        sentence[0] = re.sub("[']", '', sentence[0])
        sentence[0] = re.sub("[^\w]", ' ', sentence[0])
    return sentences

# Takes a list of sentence strings and returns an array of seperate words
# PARAMS: Sentences to break up
# RETURN: Array of list of words
def breakupSentence(sentences):
    for sentence in sentences:
        sentence[0] = re.findall("([^\s]+)", sentence[0])
    return sentences

# Takes an array of word lists and forms a vocabularity of words seen 5 or more times.
# PARAMS: Array of word lists to build vocab.
# RETURN: A one dimensional list of vocab words in alphabetical order.
def createVocabulary(wordlists):
    vocab = Vocabulary()
    for wordlist in wordlists:
        for word in wordlist[0]:
            vocab.put(word)
    vocab.buildArray()
    return vocab

# Taking a vocab list and a list of words from a sentence this function creates
# a list of length [len(vocab)+1] which contains an index for each word from the vocab
# set. Each index is either 0 (sentence doesn't contain word) or 1 (sentence contains word).
# The last index is reserved for classlabel
# ex) 1,0,1,0, ... ,1
# PARAMS: [wordlist, classLabel] list
# RETURN: Single feature in the form of [0,1,0,0,1,<classlabel>]
def createFeature(vocab, wordlist):
    feature = []
    for word in vocab.commonWords:
        if word in wordlist[0]:
            feature.append(1)
        else:
            feature.append(0)
    feature.append(int(wordlist[1]))
    return feature

# Save the designated pre-processed data to a file. The format of the file is:
# List of vocab words, ending in 'classlabel'
# List of featurized sentences seperated by commas
# PARAMS: list of sentences in feature form, output filename
# RETURN: None
def savePreprocessedData(vocab, features, filename):
    f = open(filename, 'w')
    [f.write(word + ",") for word in vocab.commonWords]
    f.write("classlabel\n")
    for feature in features:
        f.write(str(feature)[1:-1])
        f.write('\n')
    f.close()

# -----------------------
# END PREPROCCESING PHASE
# -----------------------

# --------------------------
# BEGIN CLASSIFICATION PHASE
# --------------------------

# Store each vocab word as a key in a large dictionary.
# Each dictionaries corresponding value will be an 4x3 array encapsulated by a truthtable calss
# F F - [0][0] = P(%)
# F T - [0][1] = P(%)
# T F - [1][0] = P(%)
# T T - [1][1] = P(%)
#
# Truthtable class with be able to GETPROB(0, 1) and return the corresponding probability.
# SETPROB(0, 0) = 0.02 sets probability.
# Implemented with internal 2d array
# _table variable containing zeroes to start
# INIT(name, vocab index, trainingdata):
#   loop through test data incrementing ff, ft, tf, tt, clt <classlabel true>, clf <classlabel false> via large if-elif
#   after one loop all data needed to calculate P(word | classlabel) table will be obtained
#   CreateTable(ff, ft, tf, tt, clt, clf)
#
# _name = "word from vocab"
#
# A function will formulate all of these tables by iterating through every vocab word
# and determining probabilities.
#
# With this we just pass in the truth value for BD as well as
# which vocab word and the value for the vocab word (0 or 1). we want to know the
# probabiltiy for ie) P(m|BD) and the dictionary is accessed
# via the key and then depending on whether m=true/false and bd=true/false the percentage is returned.
#
# These percentages are multiplied together to find P(bd | m, a, g, ...) as well as P(!bd | m, a, g, ...)

# These two results are compared and which ever has higher percentage then that is the guess.

# Formulate dictionary of vocab words with their associated percentages in the form of a truth table
# PARAMS: Vocab list, training data set in featurized form
# RETURN: Dictionary containing all probabilities P(word1 | sarcastic), P(word2 | sarcastic), ... etc
def train(vocab, trainingFeatures):
    bayesData = {}
    for idx, word in enumerate(vocab.commonWords):
        bayesData[word] = BayesFeature(word, idx, trainingFeatures)
        print bayesData[word].getProb(0,0),bayesData[word].getProb(0,1),bayesData[word].getProb(1,0),bayesData[word].getProb(1,1)
    return bayesData

# Looks at the vocab dictionary given the current featurized list. Tries both sarcastic=1 and sarcastic=0.
# Finds the product of each class label and chooses the most probable one.
def classify(vocab, bayesData, feature):
    true_product = 1.0
    false_product = 1.0
    for i in xrange(len(vocab.commonWords)):
        true_product += math.log10(float(bayesData[vocab.commonWords[i]].getProb(feature[i], 1)))
        false_product += math.log10(float(bayesData[vocab.commonWords[i]].getProb(feature[i], 0)))
        #print true_product
    true_product += math.log10(float(bayesData[vocab.commonWords[0]].clProb(1)))
    false_product += math.log10(float(bayesData[vocab.commonWords[0]].clProb(0)))

    print true_product
    print false_product

    if true_product >= false_product:
        return 1
    else:
        return 0

def analyzeResults():
    pass

# ------------------------
# END CLASSIFICATION PHASE
# ------------------------

def main():
    # Get raw file data
    trainingData = readRawFile("training_text.txt")
    testData = readRawFile("test_text.txt")

    # Remove symbols
    trainingData = removeSymbols(trainingData)
    testData = removeSymbols(testData)

    # Breakup into word lists
    trainingData = breakupSentence(trainingData)
    testData = breakupSentence(testData)

    # Create alphabetized array of common words
    vocab = createVocabulary(trainingData + testData)

    # Create features for each wordlist
    trainingFeatures = [createFeature(vocab, wordlist) for wordlist in trainingData]
    testFeatures = [createFeature(vocab, wordlist) for wordlist in testData]

    # Save each feature list to a file
    savePreprocessedData(vocab, trainingFeatures, "preprocessed_train.txt")
    savePreprocessedData(vocab, testFeatures, "preprocessed_test.txt")

    bayesData = train(vocab, trainingFeatures)

    print classify(vocab, bayesData, trainingFeatures[int(sys.argv[1])])


if __name__ == "__main__":
    main()
