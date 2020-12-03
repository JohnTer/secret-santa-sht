import uvicorn
from secret_santa.asgi import application
from secret_santa.settings import HOST, PORT

if __name__ == "__main__":
    uvicorn.run(application, host=HOST, port=PORT)