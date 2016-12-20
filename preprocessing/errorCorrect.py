from textblob import TextBlob,Word
def correct(text):
    t = TextBlob(text)
    return str(t.correct())

def spellcheck(text):
    txt=["She","is","mw","moom"]
    for w in txt:
        word=Word(w)
        print(word.spellcheck())