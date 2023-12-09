import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/hello-world")
def hello_world():
    # Test endpoint
    return {"hello": "world"}


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
