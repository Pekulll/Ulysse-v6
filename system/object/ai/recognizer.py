import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

class Recognizer():
    def __init__(self, language='fr-FR'):
        self.lemmatizer = WordNetLemmatizer()
        self.intents = json.loads(open(f"./system/data/language/{language}/fr-FR.json", encoding="utf-8").read())

        self.words = pickle.load(open(f"./system/data/language/{language}/words.pkl", "rb"))
        self.classes = pickle.load(open(f"./system/data/language/{language}/classes.pkl", "rb"))
        self.model = load_model(f'./system/data/language/{language}/model.h5')

    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1
        
        return np.array(bag)

    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        
        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': str(r[1])})
        
        return return_list

    def get_result(self, intents_list, intents_json):
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        
        return tag, result, int(float(intents_list[0]['probability']) * 1000) / 1000
    
    def get_result_without_neural(self, sentence):
        sentence = " ".join(self.clean_up_sentence(sentence))
        
        for item in self.intents['intents']:
            for pattern in item['patterns']:
                if pattern.lower() in sentence.lower():
                    sentence = sentence.lower().replace(pattern.lower(), "")
                    sentence = "" if sentence == None else sentence
                    return item['tag'], sentence
        
        return None, None
    
    def get_response(self, sentence, ignore_neural=False):
        if not ignore_neural:
            ints = self.predict_class(sentence)
            tag, res, probability = self.get_result(ints, self.intents)
            return tag, res, probability
        else:
            tag, result = self.get_result_without_neural(sentence)
            return tag, result, None
