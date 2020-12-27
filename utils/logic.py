from utils.bot import Evaluate
import pymongo
# from nltk.stem import WordNetLemmatizer
import nltk

#import the keywords
from utils.keyword import gender_keywords, item_keywords, budget_keywords

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["jhene-db"]

evaluate = Evaluate()
# lemmatizer = WordNetLemmatizer()

class Logic:
    def get_response(self,data):
        message = data.message.strip()
        self.message = message
        if(data.more_info):
            answers = data.answers
            context = data.from_context
            vendor = self.search_db(context,answers)
            payload = {
                    'message' : '',
                    'context' : context,
                    'more_info' : False,
                    'vendor' : vendor
                }
            return payload
        else :
            if message.lower() == 'yes':
                return {'message' : 'awn, what do you need?','context' : '', 'more_info' : False, 'vendor' : False }
            if (message.lower() == 'no') or (message.lower() == 'nope') or(message.lower() == 'nah'):
                return {'message' : 'Thank you for using Jhene','context' : '', 'more_info' : False, 'vendor' : False }
            return self.use_bot(message)

    def use_bot(self,message):
        (response, context, more) = evaluate.bot(message)
        #final answer
        if more:
            #figure our if more info can be found in the sentence
            questions = response['questions']
            (answers,requirements) = self.check_keywords(questions, context)
            if(len(requirements) == 0) :
                #you are good enough to search the database yourself
                vendor = self.search_db(context,answers)
                payload = {
                    'message' : '',
                    'context' : context,
                    'more_info' : False,
                    'vendor' : vendor
                }
                return payload
            else :
                #more info needed from the user
                final_questions = {}
                for r in requirements:
                    final_questions[r] = questions[r]
                payload = {
                    'message' : '',
                    'context' : context,
                    'answers' : answers,
                    'requirements' : requirements,
                    'more_info' : True,
                    'questions' : final_questions,
                    'vendor' : False
                }
                return payload
        payload = {'message' : response,'context' : context, 'more_info' : False, 'vendor' : False }
        return payload

    def check_keywords(self,response,context):
        requirements = ["gender","budget","location"]
        item = self.search_item(context)
        gender = budget = location = None
        if(response.get('gender')):
            gender = self.search_gender()
            if(gender):
                requirements.pop(0)
        else:
            requirements.pop(0)
        if(response.get('budget')):
            budget = self.search_budget()
            if(budget):
                requirements.pop(-2)
        else:
            requirements.pop(-2)
        if(response.get('location')):
            location = None
        else:
            requirements.pop(-1)

        answers = {
            'item' : item,
            'gender' : gender,
            'budget' : budget
        }
        return (answers,requirements)

    def search_budget(self):
        text_list = nltk.word_tokenize(self.message)[:11]
        text_lower = [w.lower() for w in text_list]
        for k in budget_keywords.keys():
            if(k in text_lower):
                return budget_keywords[k]
        return None


    def search_gender(self):
        text_list = nltk.word_tokenize(self.message)[:11]
        text_lower = [w.lower() for w in text_list]
        for k in gender_keywords.keys():
            if(k in text_lower):
                return gender_keywords[k]
        return None

    def search_item(self,context):
        text_list = nltk.word_tokenize(self.message)[:11]
        text_lower = [w.lower() for w in text_list]
        for k in item_keywords[context].keys():
            if(k in text_lower):
                return item_keywords[context][k]
        return None

    def search_db(self, context_, answers):
        print(answers)
        context = context_.split('_plug')[0]
        query = {'products' : {'$all' : [context]}}
        item = answers['item']
        if item:
            query['items_available'] = {'$all' : [item]}
        if answers['gender']:
            query['gender_for'] = {'$all' : [answers['gender']]}
        if answers['budget']:
            query['budget_for'] = {'$all': [answers['budget']]}
        # customers = db['customers'].find(query)
        #check collection and returns a user that fits at least the profile
        # for i in customers:
        #     print(i)
        return 'We currently do not have vendors that fit what you want'


def search_db():
    customers = db['customers'].find({'products' : {'$all' : ['shoes']}, 'work_locations':{'$all' : ['Akoka']}, 'owner_details' : {'gender': '1'} })
    for customer in customers:
        print(customer)

if __name__ == "__main__":
    search_db()
    print(props_keyword)
    print(gender_keyword)