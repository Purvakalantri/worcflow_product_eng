from fastapi import FastAPI
from utils.logger import logger
# from connect.connect_gmail import connect_gmail
from graph.state_graph import create_graph
import uvicorn
app=FastAPI()

@app.get("/api/reading")
def read_root():
    logger.info("Connected to FastAPI scuessfully!!")
    connect_gmail()
       
    
    return {"message":"Connected to the api successfully"}

# @app.get("/api/get_commitments")
# def get_commitments():

#     logger.info("Commitment tracking workflow started")

#     workflow = create_graph()

#     result = workflow.invoke({})

#     return {
#         "message": "Commitment tracking completed successfully",
#         "commitments": result.get("commitments", [])
#     }

@app.get("/api/get_commitments")
def get_commitments():

    logger.info("Commitment tracking workflow started")

    workflow = create_graph()

    result = workflow.invoke({})

    print("FINAL RESULT:", result)
    print("COMMITMENTS:", result.get("commitments", []))

    return {
        "message": "Commitment tracking completed successfully",
        "commitments": result.get("commitments", [])
    }

if __name__=="__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True, workers=3)