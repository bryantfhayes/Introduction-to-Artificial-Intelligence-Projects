import sys, os, random

# -------------------------
# BEGIN PREPROCESSING PHASE
# -------------------------

# Read each line of a file into a 2D array containing sentence and class label
# PARAMS: Name of the file to read. Must be in working directory.
# RETURN: 2d-Array containing sentence[0] and  classlabel[1]
def readRawFile(filename):
    pass

# Remove all apostrophes from each sentence in an array of sentences.
# PARAMS: Array of strings to clean
# RETURN: Array of original strings minus apostrophes
def removeApostrophes(sentences):
    pass

# Takes a list of sentence strings and returns an array of seperate words
# PARAMS: Sentences to break up
# RETURN: Array of list of words
def breakupSentence(sentences):
    pass

# Takes an array of word lists and forms a vocabularity of words seen 5 or more times.
# PARAMS: Array of word lists to build vocab.
# RETURN: A one dimensional list of vocab words in alphabetical order.
def createVocabulary(sentences):
    pass

# Taking a vocab list and a list of words from a sentence this function creates
# a list of length [len(vocab)+1] which contains an index for each word from the vocab
# set. Each index is either 0 (sentence doesn't contain word) or 1 (sentence contains word).
# The last index is reserved for classlabel
# ex) 1,0,1,0, ... ,1
# PARAMS: list of vocab words, a single sentence's wordlist and classlabel (2d array)
# RETURN: Single feature in the form of (0,1,0,0,1,<classlabel>)
def createFeature(vocab, sentence):
    pass

# Save the designated pre-processed data to a file. The format of the file is:
# List of vocab words, ending in 'classlabel'
# List of featurized sentences seperated by commas
# PARAMS: list of sentences in feature form, output filename
# RETURN: None
def savePreprocessedData(sentences, filename):
    pass

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
def train():
    pass

# Looks at the vocab dictionary given the current featurized list. Tries both sarcastic=1 and sarcastic=0.
# Finds the product of each class label and chooses the most probable one.
def classify():
    pass

def analyzeResults():
    pass

# ------------------------
# END CLASSIFICATION PHASE
# ------------------------

def main():
  print "Hello World"

if __name__ == "__main__":
  main()
