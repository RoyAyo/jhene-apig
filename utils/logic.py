from utils.bot import Evaluate
import pymongo
from pymongo.errors import CollectionInvalid

from utils.keyword import gender_keywords
from utils.keyword import item_keywords
from utils.keyword import budget_keywords

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["jhene-db"]

evaluate = Evaluate()

class Logic:
    def get_response(self,data):
        message = data.message.strip()
        self.message = message
        if(data.more_info):
            answers = data['answers']
            location = data['location']
            context = data['from_context']
            self.search_user(context,answers,location)
        else :
            return self.use_bot(message)

    def use_bot(self,message):
        (response, context, more) = evaluate.bot(message)
        #final answer
        if more:
            #figure our if more info can be found in the sentence
            questions = response['questions']
            (item, gender, budget) = self.check_keywords(self.message)
            if (len(questions) == 0)):
                #search database and find response (search_user)
                self.search_user(context)
                payload = {
                'message' : '',
                'context' : context,
                'more_info' : True,
                'questions' : questions
            }
            else :
                #database needed immediately
                self.search_user(context)
        payload = {'message' : response,'context' : context, more_info : False }
        return payload

    def get_responses(self):
        return "get response"

    def check_keywords(self, message):
        item = self.search_item
        budget = self.search_budget
        gender = self.search_gender
        return (item,budget,gender)

    def search_budget(self,message):
        text_list = nltk.word_tokenize(message)
        text_lower = [w.lower() for w in text_list]
        for k in budget_keywords:
            if(k in text_lower):
                return k
        return None


    def search_gender(self,message):
        text_list = nltk.word_tokenize(message)
        text_lower = [w.lower() for w in text_list]
        for k in gender_keywords:
            if(k in text_lower):
                return k
        return None

    def search_item(self,message):
        text_list = nltk.word_tokenize(message)
        text_lower = [w.lower() for w in text_list]
        for k in item_keywords:
            if(k in text_lower):
                return k
        return None

    def search_user(self, context_, answers={}, location = ''):
        context = context_.split('_')[0]
        query = {'products' : {'$all' : [context]}}
        if answers['gender']:
            gender = 1 if answers['gender'].lower() == 'female' else 2
            query['owner_details'] = {'gender' : gender}
        if answers['location'] or answers['location']:
            #find a way to get just the local govt area from geolocation lat and longs
            location = answers['location']
            query['work_locations'] = {'$all' : [location]}
        customers = db['customers'].find(query)
        #check collection and returns a user that fits at least the profile
        return "user"

    def search_product():
        return "hello"



def search_db():
    customers = db['customers'].find({'products' : {'$all' : ['shoes']}, 'work_locations':{'$all' : ['Akoka']}, 'owner_details' : {'gender': '1'} })
    for customer in customers:
        print(customer)

if __name__ == "__main__":
    search_db()
    print(props_keyword)
    print(gender_keyword)