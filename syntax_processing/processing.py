from textblob import TextBlob, Word
import nltk
_wordnet = nltk.corpus.wordnet


class TextProcessor:
    def __init__(self, initial_text):
        self.text = initial_text


    def word_tag(self, word):
        """Converts a Penn corpus tag into a Wordnet tag."""
        if word[1] in ("NN", "NNS", "NNP", "NNPS"):
            return _wordnet.NOUN
        if word[1] in ("JJ", "JJR", "JJS"):
            return _wordnet.ADJ
        if word[1] in ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ"):
            return _wordnet.VERB
        if word[1] in ("RB", "RBR", "RBS"):
            return _wordnet.ADV

        return None

    def get_sentiment(self, polarity):
        if polarity <= 0.5 and polarity >= 0:
            return "neutral"
        if polarity > 0.5:
            return "happy"

        if polarity < 0:
            return "sad"



    def processing(self):
        try:
            my_text = TextBlob(self.text)
            map_list = []
            for sentence in my_text.sentences:
                sent_tag = sentence.tags
                lemmatized_sent = []
                proper_nouns = []
                pronouns = []
                verbs = []
                processed_sentance = {}
                processed_sentance["Subject"] = ""
                processed_sentance["Predicate"] = ""
                processed_sentance["Verbs"] = ""
                for word in sent_tag:
                    w = Word(word[0].lower())
                    tag = self.word_tag(word)
                    print (w ,": ", word[1])
                    lemmatized_word = w.lemmatize(tag)
                    lemmatized_sent.append(lemmatized_word)
                    print (tag)
                    if word[1] == "NNP" or word[1] == "NNPS":
                        proper_nouns.append(lemmatized_word)
                    if word[1] == "PRP":
                        pronouns.append(lemmatized_word)
                    if tag == "v":
                        if (word[1] == "VBG" or word[1] == "VBN") and verbs[-1] == "be":
                            verbs[-1] = lemmatized_word
                        elif word[1] == "VBN" and verbs[-1] == "have":
                            verbs[-1] = lemmatized_word
                        else:
                            verbs.append(lemmatized_word)
                noun_phrase = sentence.noun_phrases

                print (lemmatized_sent)
                sentiment = self.get_sentiment(sentence.sentiment.polarity)
                processed_sentance["Sentance"] = lemmatized_sent
                processed_sentance["Sentiment"] = sentiment
                processed_sentance["Proper Nouns"] = proper_nouns
                processed_sentance["Noun Phrase"] = list(noun_phrase)
                processed_sentance["Pronouns"] = pronouns
                processed_sentance["Verbs"] = verbs

                if len(noun_phrase) != 0 and len(pronouns) != 0:
                    if lemmatized_sent.index(noun_phrase[0]) < lemmatized_sent.index(pronouns[0]):
                        processed_sentance["Subject"] = noun_phrase[0]
                    else:
                        processed_sentance["Subject"] = pronouns[0]
                elif len(noun_phrase)!=0:
                    processed_sentance["Subject"] = noun_phrase[0]
                elif len(pronouns) != 0:
                    processed_sentance["Subject"] = pronouns[0]
                if len(verbs) !=0:
                    processed_sentance["Predicate"] = verbs[0]

                map_list.append(processed_sentance)
                # print(sentiment)
            # print(map_list)
            return map_list
        except Exception as e:
            print ("Exception!")
            print (str(e))
            print (type(e))




text = "John has been living in this city since he was born."
t = TextProcessor(text)
list = t.processing()
for prop in list:
    print (prop)
