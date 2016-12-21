from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from preprocessing import *
#from semantic_processing import *
from syntax_processing import *
import nltk
nltk.data.path.append('./nltk_data/')

app = Flask(__name__)
CORS(app)

def processText(text):
    t = processing_purenltk.TextProcessor(text)
    dictionar = {}
    dictionar.update({"lang":detectLanguage.detectLang(text)})
    dictionar.update({"corrected":errorCorrect.correct(text)})
    #dictionar.update({"semantic processing":synsetSentence.semanticProcess(text)})
    dictionar.update({"syntax processing":t.processing()})
    return dictionar


@app.route('/process', methods=['POST'])
def respond():
    if "text" in request.form:
        return jsonify(processText(request.form["text"]))

@app.route('/process/<string:text>', methods=['GET'])
def respondGet(text):
    return jsonify(processText(text))


if __name__ == '__main__':
    app.run(debug=True)