from fastapi import FastAPI
from utils.logger import logger
from connect.connect_gmail import connect_gmail
import uvicorn
app=FastAPI()

@app.get("/api/reading")
def read_root():
    logger.info("Connected to FastAPI scuessfully!!")
    connect_gmail()
       
    
    return {"message":"Connected to the api successfully"}


if __name__=="__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True, workers=3)