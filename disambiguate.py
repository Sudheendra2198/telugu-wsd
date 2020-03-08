"""
    Run this script as follows: python disambiguate.py '<sentence to disambiguate>'
    It will output the result to the following files:
        input_text.txt - contains input words
        sans_stop_words.txt - contains the input text after removing stop words
        output.txt - contains the intermediate outputs of the process
        final_output.txt - contains the result
"""
import sys

import pyiwn
from googletrans import Translator

from stem import stem_words
from utils import colors


""" File initializations """
input_text=open('input_text.txt','w') # Contains the initial input text
sans_stop_words=open('sans_stop_words.txt','w') # Contains the input text after removing stop words


""" Sysnet initialization to Telugu """
iwn = pyiwn.IndoWordNet(lang=pyiwn.Language.TELUGU)

def print_line(file):
    """ 
        Used to print a seperator in the output files
    """
    file.write('\n')
    for i in range(10):
        file.write('------')

def translate_sentence(sentence):
    """ 
        Translate sentence into Telugu 
    """
    translator = Translator()
    return translator.translate(sentence,dest='telugu').text 


def get_stop_words_list():
    """ 
        Convert stop words as a list from the file - stop-words-tr.txt
    """
    stop_words = []
    with open('stop-words-tr.txt','r') as stop_word:
        for line in stop_word:
            stop_words.extend(line.split())
    return stop_words

def remove_stop_words(translated_sentence):
    """ 
        Remove stop words by comparing with stop words list
    """
    processed_words = []
    stop_words = get_stop_words_list()

    if isinstance(translated_sentence, list):
        words = translated_sentence
    else:
        words = translated_sentence.split()

    for word in words:
        input_text.write(word+'\n')
        if word not in stop_words:
            processed_words.append(word)
            sans_stop_words.write(word+'\n')
    return processed_words

def get_sense(processed_words):
    
    """
        This function takes proceesed words as input and returns best sense
        of every word.
        The algorithm applied is Lesk 
    """

    rem_synsets = []
    matcher = []
    max_cnt = 0
    max_sense = []

    op = open("output.txt","w")
    final_output = open("final_output.txt","w")

    stop_words = get_stop_words_list()
    op_dict = {}

    for word in processed_words:
        print_line(op)
        max_cnt = 0
        max_sense = iwn.synsets(word)[len(iwn.synsets(word)) - 1]
        cnt = 0

        # Get Synsets of current word
        curr_synsets = iwn.synsets(word,pos=pyiwn.PosTag.NOUN)

        # Get the remaining words and their synsets into rem_synsets
        rem_words = []
        rem_synsets = []
        for rem_word in processed_words:
            if rem_word != word:
                rem_words.append(rem_word)
        for rem_word in rem_words:
            rem_synsets.append(iwn.synsets(rem_word,pos=pyiwn.PosTag.NOUN))
        op.write('\n Rem synsets : '+str(rem_synsets))
        

        # For each synset of remaining words, 
        # generate a list of words from the meanings of the synset and its hyponyms
        # o/p : rem_to_match - list of words from the meanings of the synset and its hyponyms
        rem_to_match = []
        for synset in rem_synsets:
            for each_synset in synset:
                hyponyms = iwn.synset_relation(each_synset, pyiwn.SynsetRelations.HYPONYMY)
                for hyponym in hyponyms:
                    rem_to_match.extend(hyponym.gloss().split())
                rem_to_match.extend(each_synset.gloss().split())
        rem_to_match = remove_stop_words(rem_to_match)
        op.write('\n Rem to match : '+str(rem_to_match))
        

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
            matcher = remove_stop_words(matcher)
            op.write('\n Matcher :'+str(matcher))
            
            for matcher_word in matcher:
                if matcher_word in rem_to_match:
                    cnt += 1
                    op.write('\n Matched word : ' + str(matcher_word))
            if cnt >= max_cnt:
                max_cnt = cnt
                max_sense = synset
        final_output.write(word + ' => ' + max_sense.gloss() + '\n')
        op_dict[word] = max_sense.gloss()
    return op_dict    

if __name__ == '__main__':
    # sentence = "silk saree is beautiful"
    # sentence = "grip on subject"

    if len(sys.argv) < 2:
        print(colors.OKCYAN +  "Usage: python3 disambiguate.py '<Senetence to disambiguate>'" + colors.ENDC)
        exit(1)

    sentence = sys.argv[1]

    translated_text = translate_sentence(sentence)
    processed_words = remove_stop_words(translated_text)
    stemmed_words = stem_words(processed_words)
    print(get_sense(stemmed_words))
















