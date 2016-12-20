from flask import Flask, jsonify, request
from preprocessing import *
from semantic_processing import *
from syntax_processing import *
import nltk
nltk.data.path.append('./nltk_data/')

app = Flask(__name__)

def processText(text):
    t = processing.TextProcessor(text)
    dictionar = {}
    dictionar.update({"lang":detectLanguage.detectLang(text)})
    dictionar.update({"corrected":errorCorrect.correct(text)})
    dictionar.update({"semantic processing":synsetSentence.semanticProcess(text)})
    dictionar.update({"syntax processing":t.processing()})
    return dictionar


@app.route('/process', methods=['POST'])
def respond():
    if "text" in request.form:
        return jsonify(processText(request.form["text"]))



if __name__ == '__main__':
    app.run(debug=True)