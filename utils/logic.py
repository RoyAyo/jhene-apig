from utils.bot import Evaluate
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = myClient["jhene"]

evaluate = Evaluate()

class Logic:
    def get_response(self,data):
        message = data.message.strip()
        # self.location = data.location or ''
        if(data.from_context == ''):
            return self.use_bot(message)
        else:
            return self.get_responses()

    def use_bot(self,message):
        (response, context, more) = evaluate.bot(message)
        #final answer
        if more:
            payload = {
                'message' : '',
                'context' : context,
                'more_info' : True,
                'questions' : response
            }
        payload = {'message' : response,'context' : context, more_info : False }
        return payload

    def get_responses(self):
        return "get response"

    def search_user(self):
        businesses = mydb
        return "find user in database"