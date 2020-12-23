# from utils.bot import Evaluate
import pymongo
from pymongo.errors import CollectionInvalid
from collections import OrderedDict

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["jhene-db"]

evaluate = Evaluate()

class Logic:
    def get_response(self,data):
        message = data.message.strip()
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
            #figure our if more info is needed from user or from the database
            if (len(response['questions']) == 0) or (not response['locations']):
                payload = {
                'message' : '',
                'context' : context,
                'more_info' : True,
                'needed' : response
            }
            else :
                #database needed immediately
                self.search_user(context)
        payload = {'message' : response,'context' : context, more_info : False }
        return payload

    def get_responses(self):
        return "get response"

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



def search_db():
    customers = db['customers'].find({'products' : {'$all' : ['shoes']}, 'work_locations':{'$all' : ['Akoka']}, 'owner_details' : {'gender': '1'} })
    for customer in customers:
        print(customer)

if __name__ == "__main__":
    search_db()