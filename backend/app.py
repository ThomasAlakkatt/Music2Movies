from fastapi import FastAPI

app = FastAPI()

# The get request is what I'll see whne I go on to local host home page
# @app.get("/")
# def home():
#     return {"message": "Hello!"}



# The post request is a way for people to give requests to my website. Here, if you enter a name then you will get Hello, [NAME] back
# @app.post("/greet")
# def greet_user(name: str):
#     return {"message": "Hello, " + name + "!"}




# Curl is used like a web browser in my terminal, it helps me to make post requests directly in order to test out my FastAPI application!
# curl -X POST "http://localhost:8000/greet?name=Alice"


