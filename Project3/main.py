# Title: Sarcasm Detector
# Author: Bryant Hayes
# Last Modified: May 21st 2015
# Description: Machine learning exercise to build an AI capable of determining
#              whether or not a given sentence is sarcastic based on its
#              previous training.

import sys, os, random, re, math

# GLOBAL VARIABLES
Nx             = 1.0
Ny             = 2.0
trainingFile   = "training_text.txt"
testFile       = "test_text.txt"
ppTrainingFile = "preprocessed_train.txt"
ppTestFile     = "preprocessed_test.txt"

# -------------------------
# BEGIN PREPROCESSING PHASE
# -------------------------

# Class that represents the bayes node for each word
class BayesFeature():
    def __init__(self, word, idx, features):
        global Ny, Nx
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
                elif feature[idx] == 1:
                    self.tf += 1
            elif feature[-1] == 1:
                self.clt += 1
                if feature[idx] == 0:
                    self.ft += 1
                elif feature[idx] == 1:
                    self.tt += 1
        # Probably don't need all of tese float()'s haha
        self.probabilities = [[float(float(self.ff + Nx)/float(self.clf + Ny)),float(float(self.ft + Nx)/float(self.clt + Ny))], [float(float(self.tf + Nx)/float(self.clf + Ny)), float(float(self.tt + Nx)/float(self.clt + Ny))]]

    def getProb(self, x, y):
        return self.probabilities[x][y]

    def clProb(self, x):
        if x == 1:
            return float(self.clt) / (self.clt + self.clf)
        else:
            return float(self.clf) / (self.clt + self.clf)

# Class that represents the entire vocabulary that is used.
# Acts like a dictionary but with extra capabilities
class Vocabulary():
    def __init__(self):
        self.commonWords = []
        self._words = {}

    # Put word into the vocabulary
    def put(self, word):
        if word in self._words:
            self._words[word] += 1
        else:
            self._words[word] = 1

    # Retrieve a word from vocabulary
    def get(self, word):
        if word in self._words:
            return self._words[word]
        else:
            return 0

    # Check to see if vocabulary contains the specified word
    def contains(self, word):
        if word in self._words:
            return 1
        else:
            return 0

    # Build an alphabetized array from the word dictionary
    def buildArray(self):
        for key, val in self._words.iteritems():
            if val >= 5:
                self.commonWords.append(key)
        self.commonWords = sorted(self.commonWords)

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

# Helper function designed to rebuild the original sentences using their corresponding features.
# Used to verify features were generated correctly.
# PARAMS: feature to rebuild, vocabulary of words in feature.
# RETURN: Rebuilt sentence
def buildSentence(feature, vocab):
    sentence = [vocab.commonWords[i] for i in xrange(len(feature)-1) if feature[i]]
    return sentence

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
# Formulate dictionary of vocab words with their associated percentages in the form of a truth table
# PARAMS: Vocab list, training data set in featurized form
# RETURN: Dictionary containing all probabilities P(word1 | sarcastic), P(word2 | sarcastic), ... etc
def train(vocab, trainingFeatures):
    bayesData = {}
    for idx, word in enumerate(vocab.commonWords):
        bayesData[word] = BayesFeature(word, idx, trainingFeatures)
        #UNCOMMENT to show probabilities as they are generated.
        #print bayesData[word].getProb(0,0),bayesData[word].getProb(0,1),bayesData[word].getProb(1,0),bayesData[word].getProb(1,1)
    return bayesData

# Looks at the vocab dictionary given the current featurized list. Tries both sarcastic=1 and sarcastic=0.
# Finds the product of each class label and chooses the most probable one.
# PARAMS: vocabulary, bayesData set, the feature to classify
# RETURN: 1 if sarcastic, 0 if not sarcastic
def classify(vocab, bayesData, feature):
    true_product = false_product = 1.0
    for i in xrange(len(vocab.commonWords)):
        true_product += math.log10(float(bayesData[vocab.commonWords[i]].getProb(feature[i], 1)))
        false_product += math.log10(float(bayesData[vocab.commonWords[i]].getProb(feature[i], 0)))
    true_product += math.log10(float(bayesData[vocab.commonWords[0]].clProb(1)))
    false_product += math.log10(float(bayesData[vocab.commonWords[0]].clProb(0)))

    if true_product >= false_product:
        return 1
    else:
        return 0

# Determines how accurate the classifies was given the actual data set.
# Prints out statistics about how well the machine did.
# PARAMS: Results generated by AI, actual results
# RETURN: None
def analyzeResults(results, actual):
    falsePositives = falseNegatives = correct = 0
    for i in xrange(len(results)):
        if results[i] == actual[i]:
            correct += 1
        elif results[i] == 1 and actual[i] == 0:
            falsePositives += 1
        elif results[i] == 0 and actual[i] == 1:
            falseNegatives += 1

    print "\n"
    print "           RESULTS         "
    print "==========================="
    print " False positives:     %d" % (falsePositives)
    print " False negatives:     %d" % (falseNegatives)
    print " Correct:             %d" % (correct)
    print " Incorrect:           %d" % (falsePositives + falseNegatives)
    print " --------------------------"
    print " Accuracy:            %.2f%%" % (100 * (correct / float(falsePositives + falseNegatives + correct)))
    print "\n"


# ------------------------
# END CLASSIFICATION PHASE
# ------------------------

# Helper function: Determines what mdoe to run
# PARAMS: both sets of features (training and test)
# RETURN: selected mode
def getMode(trainingFeatures, testFeatures):
    # Check user input via command args
    if len(sys.argv) < 2:
        print "Run using: python main.py <training> or <test>"
        sys.exit(1)
    if sys.argv[1].lower() == "training":
        mode = trainingFeatures
    elif sys.argv[1].lower() == "test":
        mode = testFeatures
    else:
        print "Run using: python main.py <training> or <test>"
        sys.exit(1)
    return mode

# Program Flow
# 1) Parse test and training files for raw data
# 2) Create vocabulary
# 3) Convert each sentence into a feature [0,1,0,1,...,1]
# 4) Train AI to recognized sarcasm
# 5) Classify and Analyze results
def main():

    # Get raw file data
    trainingData = readRawFile(trainingFile)
    testData = readRawFile(testFile)

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
    savePreprocessedData(vocab, trainingFeatures, ppTrainingFile)
    savePreprocessedData(vocab, testFeatures, ppTestFile)

    # Train the AI
    bayesData = train(vocab, trainingFeatures)

    # Determine which mode to run based on command line args
    mode = getMode(trainingFeatures, testFeatures)

    # Calculate results based on either trainingFeatures or testFeatures
    results = [classify(vocab, bayesData, feature) for feature in mode]

    # Analyze results and show accuracy
    analyzeResults(results, [x[-1] for x in mode])

    #UNCOMMENT to rebuild sentences in selected set
    #print [buildSentence(mode[i], vocab) for i in xrange(len(mode))]


if __name__ == "__main__":
    main()
