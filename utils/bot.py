from nltk.stem import WordNetLemmatizer
import nltk
import pickle
import json
import random
import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.compat.v1 import get_default_graph, Session
from tensorflow.compat.v1.keras.backend import set_session
lemmatizer = WordNetLemmatizer()
from nltk.corpus import stopwords

stopwords_list = stopwords.words('english')
exclude_extra = ['plug','buy','get','vendor','around','cheap','original']
stopwords_list.extend(exclude_extra)


class Evaluate():
    def __init__(self):
        self.words_lemmatized_sorted,self.class_sorted = self.load_words()
        self.model = self.load_keras()
        self.res = self.res_json()

    def load_words(self):
        with open('model_props/words_used.pkl','rb') as f:
            words,classes = pickle.load(f)
        return (words,classes)

    def load_keras(self):
        json_file = open('model_props/bot_model.json','r')
        model_json = json_file.read()
        json_file.close()

        self.graph = get_default_graph()
        self.sess = Session()
        set_session(self.sess)
        model = model_from_json(model_json)
        model.load_weights("model_props/bot_model.h5")

        return model

    def res_json(self):
        res_file = open('model_props/res.json','r')
        res = json.load(res_file)
        # api_ = json.load(api_file)
        return res

    def bot(self,sentence):
        words_tokenized = nltk.word_tokenize(sentence)
        words_lemmatized = [lemmatizer.lemmatize(word.lower(),pos='n') for word in words_tokenized]
        words_excluded = [w for w in words_lemmatized if not w in stopwords_list]
        bag = [0] * len(self.words_lemmatized_sorted)
        for word in words_excluded:
            for i,wd in enumerate(self.words_lemmatized_sorted):
                if wd == word:
                    bag[i] = 1
                    break
        bag = np.array(bag)
        bag = bag.reshape((1,len(self.words_lemmatized_sorted)))
        with self.graph.as_default():
            set_session(self.sess)
            pred = self.model.predict(bag)
        x = pred.argmax()
        tag = self.class_sorted[x]
        print(tag)
        r = self.res[tag]
        if type(r) == dict:
            threshold = pred.max()
            print(threshold)
            if(threshold < 0.5):
                unknown_replies = ["I am not sure I get what you mean, please rephrase clearly","I don't understand you, rephrase","your english get wahala, please rephrase","I don lost, please rephrase","don't understand this one oo, rephrase abeg"]
                rand = random.randint(0,len(unknown_replies)-1)
                bot_response = unknown_replies[rand]
                return (bot_response,"",False)
            return (r,tag, True)
        else:
            rand = random.randint(0,len(r)-1)
            bot_response = r[rand]
            if (tag == 'slangs'):
                if(sentence.lower() == 'shoni cc'):
                    return ('load am, no continue song sha',tag, False)
                if(sentence.lower() == 'shoni maga'):
                    return ('bill am, no continue song sha',tag, False)
                return (sentence,tag, False)
            if (tag == "positive_feeling_response" or tag== "negative_feeling_response"):
                bot_response = bot_response + " ,What can I do for you today?"
            return (bot_response,tag, False)

if __name__ == "__main__":
    evaluate = Evaluate()
    print(evaluate.bot('ikeja'))