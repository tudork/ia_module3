from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.corpus import RegexpTokenizer

stop_words = stopwords.words("english")
tokenizer = RegexpTokenizer(r"\w+")


def semantic_info(word, lemma, context):
    #context = set(w for w in context
    #              if w != word
    #              and w != lemma)

    context.discard(word)
    context.discard(lemma)

    return simplified_lesk(lemma, context)


def synsets_for(word):
    return wn.synsets(word)


def remove_stopwords(sentence):
    return set(w for w in sentence if w not in stop_words)


def simplified_lesk(lemma, context):
    synsets = synsets_for(lemma)

    best_sense = synsets[0]
    max_common_words = 0

    if len(synsets) > 1:
        for sense in synsets:
            search_text = [use_ex for use_ex in sense.examples()]
            search_text.append(sense.definition())

            search_tokens = tokenizer.tokenize(" ".join(search_text))
            search_tokens = set(w.lower() for w in search_tokens
                                if w.lower() not in stop_words)

            common_words = len(search_tokens & context)
            if common_words > max_common_words:
                max_common_words = common_words
                best_sense = sense

    word_info = {}
    word_info["pos"] = best_sense.pos()

    synonyms = best_sense.lemma_names()
    synonyms = [w.replace("_", " ") for w in synonyms if w.replace("_", " ") != lemma]
    word_info["synonyms"] = synonyms

    hypernyms = best_sense.hypernyms()
    word_info["hypernyms"] = [w.replace("_", " ")
                              for hypernym in hypernyms
                              for w in hypernym.lemma_names()]

    word_info["definition"] = best_sense.definition()

    return word_info