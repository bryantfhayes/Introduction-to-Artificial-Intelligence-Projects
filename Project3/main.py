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

def train():
    pass

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
