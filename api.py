from fastapi import FastAPI, HTTPException
from evacuation_planner import EvacuationPlanner
from pathlib import Path
import asyncio

app = FastAPI()
planner = EvacuationPlanner(Path("config.json"))

@app.get("/plan/{days_ahead}")
async def get_plan(days_ahead: int):
    if days_ahead not in [0, 2, 6, 10]:
        raise HTTPException(status_code=400, detail="Invalid number of days ahead. Must be 0, 2, 6, or 10.")
    try:
        plan = await planner.plan_evacuation(days_ahead)
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to the Evacuation Planner API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
