def stem(word):
    len_8 = ['తున్నాడు']
    len_5 = ['తోంది','తుంది']
    len_2 = ['పై','లో','గా','కు']
    exceptions = {
        'అంశంపై' :'అంశం',
        'ఇంటికి' : 'గృహం', 'యింటికి' : 'గృహం', 'హౌస్' : 'గృహం',
        'వెళ్తున్నాను' : 'వెళ్ళు', 'వెళ్తున్నారు' : 'వెళ్ళు', 'వెళ్ళుతున్నాడు' : 'వెళ్ళు',
        
    }
    replace_5 = {'ానికి':'ం'}
    if len(word) >= 8:
        if word[len(word) - 8 : ] in len_8:
            word = word[ : len(word) - 8]
    if len(word) >= 5:
        if word[len(word) - 5 : ] in len_5:
            word = word[ : len(word) - 5]
        if word[len(word) - 5 : ] in replace_5:
            key = word[len(word) - 5 :]
            word = word[ : len(word) - 5]
            word = word + replace_5.get(key)
    if len(word) >= 2:
        if word[len(word) - 2 : ] in len_2:
            word = word[ : len(word) - 2]
    if word in exceptions:
        word = exceptions.get(word)
    return word

def stem_words(words):
    stemmed_words = []
    for word in words:
        stemmed_words.append(stem(word))
    c = 'అంశంపై'
    c1 = 'పై'
    print(c1[1])
    op = open('output.txt','w')
    op.write(str(stemmed_words))
    return stemmed_words

if __name__ == "__main__":
    stem_words(['అంశంపై'])