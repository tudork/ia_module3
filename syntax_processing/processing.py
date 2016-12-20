import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
_wordnet = nltk.corpus.wordnet


from nltk.stem import WordNetLemmatizer


class TextProcessor:
    def __init__(self, initial_text):
        self.text = initial_text


    def word_tag(self, word):

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



    def remove_signs(self,word_list):
        new_list = word_list
        for word in new_list:
            if word in (".",";","!","?",","):
                word_list.remove(word)
        return new_list

    def traverse(self, t, np_list):
        try:
            t.label()
        except AttributeError:
            return
        else:
            if t.label() == 'NP':
                # print('NP:' + str(t.leaves()))
                np_list.append(t.leaves())
                # print('NPhead:' + str(t.leaves()[-1]))
                for child in t:
                    self.traverse(child, np_list)

            else:
                for child in t:
                    self.traverse(child, np_list)

    def get_NP(self, np_list):
        final_list = []
        for item in np_list:
            final_expr = ""
            for word in item:
                final_expr = final_expr + word[0] + " "

            final_list.append(final_expr)
        return final_list

    def processing(self):
        wordnet_lemmatizer = WordNetLemmatizer()
        map_list = []
        try:
            sent_tokenize_list = sent_tokenize(self.text)
            for sentence in sent_tokenize_list:
                print (sentence)
                word_list = self.remove_signs(word_tokenize(sentence))
                tag_list = nltk.pos_tag(word_list)
                lemmatized_sent = []
                proper_nouns = []
                pronouns = []
                verbs = []
                nouns = []

                processed_sentance = {}
                processed_sentance["Subject"] = ""
                processed_sentance["Predicate"] = ""
                processed_sentance["Verbs"] = ""
                processed_sentance["Nouns"] = []
                processed_sentance["Numbers"] = []


                grammar = "NP: {<DT>?<JJ>*<NN>}"
                cp = nltk.RegexpParser(grammar)
                p_tree = cp.parse(tag_list)

                np_list = []
                self.traverse(p_tree, np_list)
                final_list = self.get_NP(np_list)
                processed_sentance["Noun Phrase"] = final_list

                for word in tag_list:

                    w = word[0].lower()
                    # print(word)
                    tag = self.word_tag(word)
                    print(w, ": ", word[1])
                    if tag != None:

                        lemmatized_word = wordnet_lemmatizer.lemmatize(w, tag)
                    else :
                        lemmatized_word = wordnet_lemmatizer.lemmatize(w, _wordnet.NOUN)

                    if word[1] == "NNP" or word[1] == "NNPS":
                        proper_nouns.append(lemmatized_word)
                    if word[1] == "NN" or word[1] == "NNS":
                        nouns.append(lemmatized_word)
                    if word[1] == "CD" :
                        processed_sentance["Numbers"].append(lemmatized_word)

                    if word[1] == "PRP":
                        pronouns.append(lemmatized_word)
                    if tag == "v":
                        if (word[1] == "VBG" or word[1] == "VBN") and verbs[-1] == "be":
                            verbs[-1] = lemmatized_word
                        elif word[1] == "VBN" and verbs[-1] == "have":
                            verbs[-1] = lemmatized_word
                        else:
                            verbs.append(lemmatized_word)
                    if tag == "n" :
                        processed_sentance["Nouns"].append(lemmatized_word)


                    lemmatized_sent.append(lemmatized_word)
                    processed_sentance["Sentance"] = lemmatized_sent
                    processed_sentance["Proper Nouns"] = proper_nouns
                    # processed_sentance["Noun Phrase"] = list(noun_phrase)
                    processed_sentance["Pronouns"] = pronouns
                    processed_sentance["Verbs"] = verbs


                if len(processed_sentance["Nouns"]) != 0 and len(pronouns) != 0:
                    if lemmatized_sent.index(processed_sentance["Nouns"][0]) < lemmatized_sent.index(pronouns[0]):
                        processed_sentance["Subject"] = processed_sentance["Nouns"][0]
                    else:
                        processed_sentance["Subject"] = pronouns[0]
                elif len(processed_sentance["Nouns"]) != 0:
                    processed_sentance["Subject"] = processed_sentance["Nouns"][0]
                elif len(pronouns) != 0:
                    processed_sentance["Subject"] = pronouns[0]
                if len(verbs) != 0:
                    processed_sentance["Predicate"] = verbs[0]

                map_list.append(processed_sentance)
            return map_list

        except Exception as e:
            print("Exception!")
            print(str(e))
            print(type(e))





#text = "The little boy has been living in this city for 10 years. He has a small dog."
#t = TextProcessor(text)
#lista = t.processing()
#for prop in lista:
#    print(str(prop))


