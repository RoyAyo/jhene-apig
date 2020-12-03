from utils.bot import Evaluate

evaluate = Evaluate()


class Logic:
    def get_response(self,data):
        message = data['message'].strip()
        self.location = data.get('location')
        if(data['from_context'] == ''):
            return self.use_bot(message)
        else:
            return self.use_api_analyzer(data['from_context'],data['context_response'])

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
                message = self.use_api_analyzer(context['from'],context['parameters'])
                payload = {'message' : response,'context' : '','bot_questions':{}}
                return payload

    def use_api_analyzer(self,context,parameters=[]):
        print('okay')
        return "hello world"