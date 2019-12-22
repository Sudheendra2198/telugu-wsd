"""
    Run this script as follows: python build_stop_words.py <stop word to add>
    Ex:-  python build_stop_words.py inside
    will add the telugu translation of "inside" to stop-words-tr.txt
"""
import sys
from googletrans import Translator

""" Translate stop word into Telugu """
translator = Translator()
s = translator.translate(sys.argv[1],dest='te')

""" Append stop word to file """
f = open('stop-words-tr.txt','a')
f.write('\n'+s.text)

""" Translated a file containing English stop words to Telugu """
""" with open('stop-words-en.txt','r') as sw:
    with open('stop-words-tr.txt','w') as n:
        for line in sw:
            trans = translator.translate(line,dest='te')
            n.write(trans.text+'\n') """

