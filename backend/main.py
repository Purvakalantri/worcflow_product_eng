from fastapi import FastAPI
from utils.logger import logger
from graph.state_graph import create_graph
from fastapi.middleware.cors import CORSMiddleware
from connect.calendar_event import add_calendar_event
from connect.save_commits import save_calendar
import uvicorn

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/reading")
def read_root():
    logger.info("Connected to FastAPI scuessfully!!")    
    
    return {"message":"Connected to the api successfully"}

@app.get("/api/get_commitments")
def get_commitments():

    logger.info("Commitment tracking workflow started")

    workflow = create_graph()

    result = workflow.invoke({})

    # print("FINAL RESULT:", result)
    # print("COMMITMENTS:", result.get("commitments", []))

    return {"message": "Commitment tracking completed successfully", 
    "commitments": result.get("commitments", [])}

@app.post("/api/calendar/add")
def add_to_calendar(data: dict):

    event = add_calendar_event(
        task=data["task"],
        due_date=data["due_date"],
        recipient_email=data["recipient_email"],
        user_email= data["user_email"],
        requirements=data.get("requirements", [])
    )
    # print("event",event)
    save_calendar(commitment=data, event_id=event["event_id"], event_link=event["event_link"])
    return {"message": "Event added to Google Calendar","event": event}


if __name__=="__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True, workers=3)