from textblob import TextBlob, Word
from textblob.wordnet import VERB,NOUN,ADJ,ADV
import nltk
#TextBlob.correct() are o acuratete de 70%...in general greseste la nume...
# tb sa determin partile de vorbire ca atunci cand modific sa ramana aceeasi parte de vorbire
#detect language imi da raportul cel mai mare dintr-un text
class Preprocesare:

    def correct_sentence(text):
        t=TextBlob(text)
        return t.correct()
    def spell_checkers(text):
        t=TextBlob(text)
        w=Word(t)
        print(w.spellcheck())
    def validate_language(selftext):
        return True



#print(Preprocesare.correct_sentence("I hawe an cat"))
#Preprocesare.spell_checkers("I have a grey cat")