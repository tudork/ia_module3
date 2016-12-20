from textblob import TextBlob, Word
from textblob.wordnet import VERB,ADV,ADJ,NOUN


#text="Ana is here. She is happy."
def semanticProcess(text):
    t=TextBlob(text)
    tags = []
    synset = {}
    #for word in t.tags:
    #    word=word[0].lower()
    #    print(word)
    #    w=Word(word[0])
    #    print(w.get_synsets())
    for word in t.tags:
        tags.append(word)
        #synset.setdefault(word[0], Word(word[0]).get_synsets())

    dictionar = {"tags":tags, "synset":synset}
    return dictionar


