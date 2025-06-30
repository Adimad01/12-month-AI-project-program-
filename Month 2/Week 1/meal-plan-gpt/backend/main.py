from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from planner import generate_meal_plan

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MealRequest(BaseModel):
    diet: str
    calories: int
    days: int = 7

@app.post("/generate")
def generate(req: MealRequest):
    plan = generate_meal_plan(req.diet, req.calories, req.days)
    print("✅ Meal plan printed in terminal.")
    return plan  # ⬅️ on renvoie le plan à React
