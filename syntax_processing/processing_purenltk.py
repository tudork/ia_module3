import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
_wordnet = nltk.corpus.wordnet
from semantic_processing import semantic_processing as semantics

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

                # print (sentence)
                word_list = self.remove_signs(word_tokenize(sentence))
                tag_list = nltk.pos_tag(word_list)
                lemmatized_sent = []
                proper_nouns = []
                pronouns = []
                verbs = []
                nouns = []

                processed_sentence = {}
                processed_sentence["original_sentence"] = sentence
                processed_sentence["subject"] = ""
                processed_sentence["predicate"] = ""
                processed_sentence["verbs"] = ""
                processed_sentence["nouns"] = []
                processed_sentence["numbers"] = []

                grammar = "NP: {<DT>?<JJ>*<NN>}"
                cp = nltk.RegexpParser(grammar)
                p_tree = cp.parse(tag_list)

                np_list = []
                self.traverse(p_tree, np_list)
                final_list = self.get_NP(np_list)
                processed_sentence["noun_phrases"] = final_list

                for word in tag_list:

                    w = word[0].lower()
                    # print(word)
                    tag = self.word_tag(word)
                    # print(w, ": ", word[1])
                    if tag != None:

                        lemmatized_word = wordnet_lemmatizer.lemmatize(w, tag)
                    else :
                        lemmatized_word = wordnet_lemmatizer.lemmatize(w, _wordnet.NOUN)

                    if word[1] == "NNP" or word[1] == "NNPS":
                        proper_nouns.append(lemmatized_word)
                    if word[1] == "NN" or word[1] == "NNS":
                        nouns.append(lemmatized_word)
                    if word[1] == "CD" :
                        processed_sentence["numbers"].append(lemmatized_word)

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
                        processed_sentence["nouns"].append(lemmatized_word)


                    lemmatized_sent.append(lemmatized_word)
                    processed_sentence["sentence"] = lemmatized_sent
                    processed_sentence["proper_nouns"] = proper_nouns
                    # processed_sentance["Noun Phrase"] = list(noun_phrase)
                    processed_sentence["pronouns"] = pronouns
                    processed_sentence["verbs"] = verbs

                if len(processed_sentence["nouns"]) != 0 and len(pronouns) != 0:
                    if lemmatized_sent.index(processed_sentence["nouns"][0]) < lemmatized_sent.index(pronouns[0]):
                        processed_sentence["subject"] = processed_sentence["nouns"][0]
                    else:
                        processed_sentence["subject"] = pronouns[0]
                elif len(processed_sentence["nouns"]) != 0:
                    processed_sentence["subject"] = processed_sentence["nouns"][0]
                elif len(pronouns) != 0:
                    processed_sentence["subject"] = pronouns[0]
                if len(verbs) != 0:
                    processed_sentence["predicate"] = verbs[0]

                processed_sentence["semantics"] = {}
                word_list = [w.lower() for w in word_list]
                context = semantics.remove_stopwords(word_list)
                lemmas = semantics.remove_stopwords(lemmatized_sent)
                for lemma in lemmas:
                    processed_sentence["semantics"].setdefault(lemma, semantics.semantic_info(lemma, lemma, context))

                map_list.append(processed_sentence)
            return map_list

        except Exception as e:
            print("Exception!")
            print(str(e))
            print(type(e))





#text = "He is my brother."
#t = TextProcessor(text)
#lista = t.processing()
#for prop in lista:
#    print(str(prop))


