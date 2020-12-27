from locust import HttpUser, task

class MyUser(HttpUser):
    @task
    def get_home(self):
        self.client.get("/")
            
    @task(3)
    def predict(self):
        payload = {
            "message" : "get a tailor to sew my gown",
            "from_context" : "",
            "more_info" : False,
            "answers" : [],
        	"location" : ""
        }
        self.client.post("/send_message", json=payload)