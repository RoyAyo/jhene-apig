from utils.bot import Evaluate
import pymongo
from pymongo.errors import CollectionInvalid
from collections import OrderedDict

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["jhene"]

evaluate = Evaluate()

user_schema = {

}

class Logic:
    def get_response(self,data):
        message = data.message.strip()
        if(data.more_info):

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

    def search_user(self, context):
        businesses = mydb
        #check collection and returns a user that fits at least the profile
        return "user"
