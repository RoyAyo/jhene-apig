from utils.bot import Evaluate

evaluate = Evaluate()


class Logic:
    def get_response(self,data):
        message = data.message.strip()
        # self.location = data.location or ''
        if(data.from_context == ''):
            print('here')
            return self.use_bot(message)
        else:
            return self.get_responses()

    def use_bot(self,message):
        (response, context) = evaluate.bot(message)
        if (type(response) == str):
            #final answer
            payload = {'message' : response,'context' : '','bot_questions':{}}
            return payload
        else: 
            #check if more responses are needed
            if(len(message["response"]) > 0 ):
                payload = {'message' : '','context' : context,'bot_questions' : response}
                return payload
            else:
                payload = {'message' : response,'context' : '','bot_questions':{}}
                return payload

    def get_responses(self):
        return "get response"