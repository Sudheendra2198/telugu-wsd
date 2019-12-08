from googletrans import Translator
translator = Translator()
s = translator.translate("goat is eating",dest='te')
print(s.text)
