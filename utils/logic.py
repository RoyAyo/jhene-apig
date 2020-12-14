from utils.bot import Evaluate

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
        (response, context) = evaluate.bot(message)
        #final answer
        payload = {'message' : response,'context' : context}
        return payload

    def get_responses(self):
        return "get response"