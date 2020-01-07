"""
    Run this script as follows: python process.py
    It will output the result to files
    input_text.txt contains input words
    sans_stop_words.txt contains the input text after removing stop words
    synset.txt contains the output of matched synset
"""

import nltk
import pyiwn
from nltk.tokenize import PunktSentenceTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from krovetzstemmer import Stemmer
from nltk.corpus import wordnet
from googletrans import Translator


""" File initializations """
input_text=open('input_text.txt','w') # Contains the initial input text
sans_stop_words=open('sans_stop_words.txt','w') # Contains the input text after removing stop words
synset_output=open('synset.txt','w') # Contains the output of matched synset
sense_output=open('sense_output.txt','w')

""" Sysnet initialization to Telugu"""
iwn = pyiwn.IndoWordNet(lang=pyiwn.Language.TELUGU)
stemmer = Stemmer()

def print_line(file):
    file.write('\n')
    for i in range(10):
        file.write('------')

def stem_input(words):
    stems = []
    for w in words:
        print(stemmer.stem(w))
        stems.append(stemmer.stem(w))
    return stems

def translate_stems(stems):
    """ Translate input into Telugu """
    translated_words = []
    translator = Translator()
    for stem in stems:
        translated_words.append(translator.translate(stem,dest='te').text) # Enter input in this line
    return translated_words

def translate_sentence(sentence):
    translator = Translator()
    return translator.translate(sentence,dest='te').text

def get_stop_words_list():
    """ Convert stop words as a list """
    stop_words = []
    with open('stop-words-tr.txt','r') as stop_word:
        for line in stop_word:
            stop_words.extend(line.split())
    return stop_words

def remove_stop_words(translated_words):
    """ Remove stop words """
    processed_words = []
    stop_words = get_stop_words_list()
    words = translated_words
    for word in words:
        input_text.write(word+'\n')
        if word not in stop_words:
            processed_words.append(word)
            sans_stop_words.write(word+'\n')
    return processed_words

def get_sense(processed_words):
    rem_words = []
    rem_synsets = []
    rem_to_match = []
    matcher = []
    max_cnt = 0
    max_sense = []
    op = open("output.txt","a")
    final_output = open("final_output.txt","w")
    for word in processed_words:
        cnt = 0

        # Get Synsets of current word
        curr_synsets = iwn.synsets(word,pos=pyiwn.PosTag.NOUN)

        # Get the remaining words and their synsets into rem_synsets
        for rem_word in processed_words:
            if rem_word != word:
                rem_words.append(rem_word)
        for rem_word in rem_words:
            rem_synsets = (iwn.synsets(rem_word,pos=pyiwn.PosTag.NOUN))
        op.write('\n'+str(rem_synsets))
        print_line(op)

        # For each synset of remaining words, 
        # generate a list of words from the meanings of the synset and its hyponyms
        # o/p : rem_to_match - list of words from the meanings of the synset and its hyponyms
        for synset in rem_synsets:
            hyponyms = iwn.synset_relation(synset, pyiwn.SynsetRelations.HYPONYMY)
            for hyponym in hyponyms:
                rem_to_match.extend(hyponym.gloss().split())
            rem_to_match.extend(synset.gloss().split())
        op.write('\n'+str(rem_to_match))
        print_line(op)

        # For each synset of current word,
        # match the words from its meaning to all the words in rem_to_match
        # If count matches increment it and if it is maximum, it is taken as the sense
        for synset in curr_synsets:
            matcher = []
            cnt = 0
            hyponyms = iwn.synset_relation(synset, pyiwn.SynsetRelations.HYPONYMY)
            for hyponym in hyponyms:
                matcher.extend(hyponym.gloss().split())
            matcher.extend(synset.gloss().split())
            op.write('\n'+str(matcher))
            print_line(op)
            for matcher_word in matcher:
                if matcher_word in rem_to_match:
                    cnt += 1
            if cnt >= max_cnt:
                max_cnt = cnt
                max_sense = synset
        final_output.write(word + '=>' + max_sense.gloss() + ' : '+str(max_cnt)+'\n')

if __name__ == '__main__':
    # words = word_tokenize("grip on subject")
    words = word_tokenize("silk saree is beautiful")
    stems = stem_input(words)
    translated_words = translate_stems(stems)
    processed_words = remove_stop_words(translated_words)
    get_sense(processed_words)













