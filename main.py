from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to my API!!!"}


@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}


@app.post
def create_posts():
    return {"message": "Succesfully created posts"}
