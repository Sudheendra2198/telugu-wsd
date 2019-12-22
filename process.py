"""
    Run this script as follows: python process.py
    It will output the result to files
    input_text.txt contains input words
    sans_stop_words.txt contains the input text after removing stop words
    synset.txt contains the output of matched synset
"""
from googletrans import Translator
import pyiwn

""" File initializations """
input_text=open('input_text.txt','w') # Contains the initial input text
sans_stop_words=open('sans_stop_words.txt','w') # Contains the input text after removing stop words
synset_output=open('synset.txt','w') # Contains the output of matched synset

""" Sysnet initialization to Telugu"""
iwn = pyiwn.IndoWordNet(lang=pyiwn.Language.TELUGU)

""" Translate input into Telugu """
translator = Translator()
translated_input = translator.translate("silk saree is beautiful",dest='te') # Enter input in this line

""" Convert stop words as a list """
stop_words = []
with open('stop-words-tr.txt','r') as stop_word:
    for line in stop_word:
        stop_words.extend(line.split())


""" Remove stop words """
processed_words = []
words = translated_input.text.split()
for word in words:
    input_text.write(word+'\n')
    if word not in stop_words:
        processed_words.append(word)
        sans_stop_words.write(word+'\n')

for word in processed_words:
    synset_output.write('\n'+str(iwn.synsets(word)))




