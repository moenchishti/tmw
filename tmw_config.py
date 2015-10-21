#!/usr/bin/env python3
# Filename: my_tmw.py
# Author: #cf

##################################################################
###  CONFIG FILE for: Topic Modeling Workflow (tmw)            ###
##################################################################

# Used in the following paper: 
# Christof Schoech, "Topic Modeling French Crime Fiction",
# presented at the Digital Humanities Conference, Sydney, 2015.
# For information on requirements and usage, see the README file.

# This config file is structured as follows: 
# 0. General Settings
# 1. Preprocessing Texts
# 2. Topic Modeling
# 3. Posprocessing Data
# 4. Basic Visualizations
# 5. Advanced Visualizations
# 6. Other / Obsolete / in development

# You may find a tutorial explaining the purpose of each function 
# as well as its input, output and other parameters at: 
# https://www.penflip.com/c.schoech/tmw-tutorial


################################
### GENERAL SETTINGS         ###
################################

### The following settings depend on the system used.
### Path to the working directory.
wdir = "/home/" # end with slash.
### Path to the TreeTagger file (language-dependent!)
tagger = "/home/[USER]/Programs/TreeTagger/cmd/tree-tagger-french"
### Path to Mallet installation directory
mallet_path = "/home/[USER]/Programs/Mallet/bin/mallet"
### Path to the font for wordle generation
font_path = "/home/[USER]/.fonts/AlegreyaSans-Regular.otf"

import tmw
#print(help(topmod))



################################
###    PREPROCESSING TEXTS   ###
################################

### tei5reader_fulldocs (standard option)
### Extract selected plain text from XML/TEI files.
inpath = wdir + "master/*.xml"
outfolder = wdir + "1_txt/"
#tmw.tei5reader_fulldocs(inpath,outfolder)

### segmenter
### Split entire texts into smaller segments.
inpath = wdir + "1_txt/*.txt"
outfolder = wdir + "2_segs/"
target = 600
sizetolerancefactor = 1.1
preserveparagraphs = True
#tmw.segmenter(inpath, outfolder, target, sizetolerancefactor, preserveparagraphs)

### segments_to_bins
### Assign each segment to one bin over textual progression.
inpath = wdir + "2_segs/*.txt"
outfolder = wdir + "7_aggregates/"
binsnb = 3 # number of bins
#tmw.segments_to_bins(inpath,outfolder, binsnb)

### pretokenize
### Perform some preliminary tokenization.
inpath = wdir + "2_segs/*.txt"
outfolder = wdir + "3_tokens/"
substitutionsFile = wdir+"extras/fr_pretokenize_subs.csv"
#tmw.pretokenize(inpath, substitutionsFile, outfolder)

### call_treetagger
### Perform lemmatization and POS tagging.
infolder = wdir + "2_segs/"
outfolder = wdir + "4_tagged/"
tagger = tagger
#tmw.call_treetagger(infolder, outfolder, tagger) 

### make_lemmatext
### Extract selected lemmata from tagged text.
inpath = wdir + "4_tagged/*.trt"
outfolder = wdir + "5_lemmata/"
mode = "frN" # frN=nouns, esN=nouns, frNV=nouns+verbs, frNVAA=nouns+verbs+adj+adverbs 
stoplist_errors = wdir+"extras/fr_stopwords_errors.txt" # wdir
#tmw.make_lemmatext(inpath, outfolder, mode, stoplist_errors)

### substitute
### Perform some preliminary tokenization.
inpath = wdir + "5_lemmata/*.txt"
outfolder = wdir + "5_substituted/"
substitutionsFile = wdir+"extras/fr_argot-substitutions.csv"
#tmw.substitute(inpath, substitutionsFile, outfolder)


################################
###    TOPIC MODELING        ###
################################

### call_mallet_import
### Imports text data into the Mallet corpus format.
mallet_path = mallet_path
infolder = wdir + "5_substituted/"
outfolder = wdir + "6_mallet/" 
outfile = outfolder + "corpus.mallet"
stoplist_project = wdir+"extras/fr_stopwords_project.txt" # in tmw folder
#tmw.call_mallet_import(mallet_path, infolder, outfolder, outfile, stoplist_project)

### call_mallet_model
### Performs the actual topic modeling. 
mallet_path = mallet_path
inputfile = wdir + "6_mallet/corpus.mallet"
outfolder = wdir + "6_mallet/"
numOfTopics = "250" # string
optimize_interval = "100" # string
num_iterations = "5000" # string
num_top_words = "100" # string
doc_topics_max = numOfTopics
num_threads = "4" # string
#tmw.call_mallet_modeling(mallet_path, inputfile, outfolder, numOfTopics, optimize_interval, num_iterations, num_top_words, doc_topics_max)



################################
###    POSTPROCESSING DATA   ###
################################

### create_mastermatrix
### Creates a matrix with all information (metadata and topic scores for 
### each segment) in one place.
corpuspath = wdir+"2_segs/*.txt"
outfolder = wdir+"7_aggregates/"
mastermatrixfile = "mastermatrix.csv"
metadatafile = wdir+"metadata.csv"
topics_in_texts = wdir+"6_mallet/topics-in-texts.csv"
numOfTopics = int(numOfTopics)
useBins = True # True|False
binDataFile = wdir+"7_aggregates/segs-and-bins.csv"
###tmw.create_mastermatrix(corpuspath, outfolder, mastermatrixfile, metadatafile, topics_in_texts, numOfTopics, useBins, binDataFile)

### calculate_averageTopicScores
### Based on the mastermatrix, calculates various average topic score datasets.
mastermatrixfile = wdir+"/7_aggregates/mastermatrix.csv"
outfolder = wdir+"7_aggregates/"
targets = ["segmentID"] 
#targets = ["subgenre", "author-name", "subsubgenre","decade", "narration", "setting", "author-gender", "title", "protagonist-policier"] 
#targets = ["author", "author-gender", "title", "decade", "subgenre", 
#           "idno", "segmentID", "narration", "protagonist-policier", "binID"] 
#tmw.calculate_averageTopicScores(mastermatrixfile, targets, outfolder)

### calculate_complexAverageTopicScores
### Based on the mastermatrix, calculates average topic scores for two target categories at once.
mastermatrixfile = wdir+"/7_aggregates/mastermatrix.csv"
outfolder = wdir+"7_aggregates/"
targets = ["decade", "binID"] # 2 targets to combine
#tmw.calculate_complexAverageTopicScores(mastermatrixfile, targets, outfolder)

### save_firstWords
### Saves the first words of each topic to a separate file.
topicWordFile = wdir+"6_mallet/topics-with-words.csv"
outfolder = wdir+"7_aggregates/"
filename = "firstWords.csv"
#tmw.save_firstWords(topicWordFile, outfolder, filename)

### save_topicRanks
### Saves the rank (in the overall scores) of each topic to a separate file.
topicWordFile = wdir+"6_mallet/topics-with-words.csv"
outfolder = wdir+"7_aggregates/"
filename = "topicRanks.csv"
tmw.save_topicRanks(topicWordFile, outfolder, filename)



################################
###  BASIC VISUALIZATION     ###
################################

### make_wordle_from_mallet
### Creates a wordle for each topic.
word_weights_file = wdir+"6_mallet/" + "word-weights.txt"
topicRanksFile = wdir + "7_aggregates/" + "topicRanks.csv"
numOfTopics = numOfTopics
words = 40
outfolder = wdir+"8_visuals/wordles/"
font_path = font_path
dpi = 300
#tmw.make_wordle_from_mallet(word_weights_file,numOfTopics, words,outfolder, topicRanksFile, font_path,dpi)

### crop_images
### Optional. Crops the wordle image files.
inpath = wdir + "8_visuals/wordles/*.png"
outfolder = wdir + "8_visuals/wordles/"
left = 225 # image start at the left
upper = 210 # image start at the top
right = 2225 # image end on the right
lower = 1310 # image end at the bottom
#tmw.crop_images(inpath, outfolder, left, upper, right, lower)

### plot_topTopics
### For each item from a category, creates a barchart of the top topics.
averageDatasets = wdir+"7_aggregates/avg*.csv" 
firstWordsFile = wdir+"7_aggregates/firstWords.csv"
targetCategories = ["title"]
topTopicsShown = 16 
numOfTopics = numOfTopics 
fontscale = 1.0
height = 0 # 0=automatic and variable
dpi = 300
mode = "normalized" #normalized|zscores|absolute
outfolder = wdir+"/8_visuals/topTopics/"
tmw.plot_topTopics(averageDatasets, firstWordsFile, numOfTopics, targetCategories, mode, topTopicsShown, fontscale, height, dpi, outfolder)

### plot_topItems ###
### For each topic, creates a barchart with top items from a category. 
averageDatasets = wdir+"7_aggregates/avg*.csv" 
outfolder = wdir+"8_visuals/topItems/"
firstWordsFile = wdir+"7_aggregates/firstWords.csv"
numOfTopics = numOfTopics # must be actual number of topics modeled. 
targetCategories = ["segmentID"] 
topItemsShown = 20 
fontscale = 0.8
height = 0 # 0=automatic and flexible
dpi = 300
#tmw.plot_topItems(averageDatasets, outfolder, firstWordsFile, numOfTopics, targetCategories, topItemsShown, fontscale, height, dpi)



################################
###  ADVANCED VISUALIZATION  ###
################################

### plot_distinctiveness_heatmap ###
### For each category, make a heatmap of most distinctive topics. 
averageDatasets = wdir+"7_aggregates/avg*.csv" 
firstWordsFile = wdir+"7_aggregates/firstWords.csv"
outfolder = wdir+"8_visuals/distinctiveness/"
targetCategories = ["protagonist-policier"] 
mode = "zscores" #normalized|zscores|absolute
numOfTopics = numOfTopics # actual number of topics modeled.
topTopicsShown = 20 
fontscale = 1.0
dpi = 300
#tmw.plot_distinctiveness_heatmap(averageDatasets, firstWordsFile, mode, outfolder, targetCategories, numOfTopics, topTopicsShown, fontscale, dpi)

### plot_topicsOverTime ###
###     
averageDatasets = wdir+"7_aggregates/avgtopicscores_by-decade.csv" 
firstWordsFile = wdir+"7_aggregates/firstWords.csv"
outfolder = wdir+"8_visuals/overTime/"
numOfTopics = numOfTopics # actual number of topics modeled.
fontscale = 1.0
dpi = 300
height = 0 # for lineplot; 0=automatic
mode = "line" # area|line for areaplot or lineplot
topics = ["190", "6"] # list of one or several topics
#tmw.plot_topicsOverTime(averageDatasets, firstWordsFile, outfolder, numOfTopics, fontscale, dpi, height, mode, topics)

### topicClustering ###
# This function will create a dendrogram grouping topics based on their word weight similarity.
wordWeightsFile = wdir+"6_mallet/"+"word-weights.txt"
outfolder = wdir+"8_visuals/clustering/"
topicsToUse = numOfTopics # should be all topics.
wordsPerTopic = 50
methods=["weighted"] # list
metrics=["cosine"] # list
#tmw.topicClustering(wordWeightsFile, wordsPerTopic, outfolder, methods, metrics, topicsToUse)

### itemClustering ###
# This function creates a dendrogram of items in a category (authors, titles).
averageDatasets = wdir+"7_aggregates/avg*.csv" 
figsize = (15,10) # width,height
outfolder = wdir+"8_visuals/clustering/"
topicsPerItem = 50 # can be set
sortingCriterium = "mean" # std|mean
targetCategories = ["author-name"] # list
methods=["weighted"] # list
metrics=["cosine"] # list
#tmw.itemClustering(averageDatasets, figsize, outfolder, topicsPerItem, targetCategories, methods, metrics, sortingCriterium)

### simpleProgression ###
### Creates a lineplot of topic development over textual progression.
averageDataset = wdir+"7_aggregates/avgtopicscores_by-binID.csv" 
firstWordsFile = wdir+"7_aggregates/firstWords.csv"
outfolder = wdir+"8_visuals/progression/simple/"
numOfTopics = numOfTopics # must be actual number of topics modeled.
fontscale = 1.0
dpi = 300
height = 0 # 0=automatic
mode = "sel" # all|sel 
topics = ["25", "44", "12"] # if mode="sel": list of topics
#tmw.simpleProgression(averageDataset, firstWordsFile, outfolder, numOfTopics, fontscale, dpi, height, mode, topics)

### complexProgression ###
### Creates a lineplot of topic development over textual progression, 
### but does so separatedly for different target categories.
averageDataset = wdir+"7_aggregates/complex-avgtopicscores_by-subgenre+binID.csv" 
firstWordsFile = wdir+"7_aggregates/firstWords.csv"
outfolder = wdir+"8_visuals/progression/complex/"
numOfTopics = numOfTopics # must be actual number of topics modeled.
targetCategories = ["subgenre","binID"] # two values, corresponding to averageDataset
fontscale = 1.0
dpi = 300
height = 0 # for lineplot; 0=automatic
mode = "all" # all|sel ### only "all" is implemented ##
#tmw.complexProgression(averageDataset, firstWordsFile, outfolder, numOfTopics, targetCategories, fontscale, dpi, height, mode, topics)



################################
###  OTHER / OBSOLETE / DEV  ###
################################

### 5c show segment
## To read a specific segment, better than looking in the folder.
segmentID = "rf1246§0048" # indicate here, manually
outfolder = wdir+"/9_sel-segs/"
#tmw.show_segment(wdir,segmentID, outfolder)

### itemPCA ### CURRENTLY NOT WORKING
averageDatasets = wdir+"7_aggregates/avg*.csv" 
figsize = (10,10) # width,height
outfolder = wdir+"8_visuals/clustering/"
topicsPerItem = 50
sortingCriterium = "std" # std|mean
targetCategories = ["subgenre"] # list
methods=["weighted"] # list
metrics=["cosine"] # list
#tmw.itemPCA(averageDatasets, targetCategories, topicsPerItem, sortingCriterium, figsize, outfolder)
