from langdetect import detect, language, detect_langs, DetectorFactory
from textblob import TextBlob

language_validation_limit= language.Language('en',0.8)
DetectorFactory.seed = 0
def detectLang(text):
    result = detect_langs(text)
    print(result)
    lang = detect(text)
    probable_language = result[0]
    if lang=='en' and probable_language > language_validation_limit:
        return 'en'
    else:
        return 'other'
def translate():
    # Method two with translate
    txt=TextBlob(text)
    myTxt=txt.translate(to="en")
    if myTxt==txt:
        print("It's english")
    else:
        print("Is another language")

#print (detectLang("Is just a text to test a request what is wrong with you?"))