from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import random
from datetime import datetime
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://astrology-webapp-alpha.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = Path("punishments.json")


class Punishment(BaseModel):
    id: int
    content: str
    category: str
    createdAt: str


class PunishmentCreate(BaseModel):
    content: str
    category: str


def load_data():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.get("/punishments", response_model=List[Punishment])
def get_punishments(category: Optional[str] = None):
    data = load_data()
    if category:
        data = [p for p in data if p["category"] == category]
    return data


@app.get("/punishments/random", response_model=Punishment)
def get_random_punishment(category: Optional[str] = None):
    data = load_data()
    if category:
        data = [p for p in data if p["category"] == category]

    if not data:
        raise HTTPException(status_code=404, detail="No punishments found")

    return random.choice(data)


@app.post("/punishments", response_model=Punishment)
def create_punishment(punishment: PunishmentCreate):
    data = load_data()

    new_id = max([p["id"] for p in data], default=0) + 1

    new_punishment = {
        "id": new_id,
        "content": punishment.content,
        "category": punishment.category,
        "createdAt": datetime.utcnow().isoformat(),
    }

    data.append(new_punishment)
    save_data(data)
