import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes.api import router as api_router

app = FastAPI()

origins = ["http://localhost:8005"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == '__main__':
    # Run the FastAPI application using Uvicorn
    uvicorn.run("main:app", host='127.0.0.1', port=8005, log_level="info", reload=True)
    # print("running")
