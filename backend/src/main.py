# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from sqlalchemy import func
# from pydantic import BaseModel
# from typing import List, Optional
# from datetime import datetime
# from pathlib import Path
# import json
# import random

# from database import engine, Base, AsyncSessionLocal
# from model import Punishment
# from schemas import PunishmentCreate, PunishmentResponse

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://astrology-webapp-alpha.vercel.app"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# DATA_FILE = Path("punishments.json")


# class Punishment(BaseModel):
#     id: int
#     content: str
#     category: str
#     createdAt: str


# class PunishmentCreate(BaseModel):
#     content: str
#     category: str


# def load_data():
#     if not DATA_FILE.exists():
#         return []
#     with open(DATA_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)


# def save_data(data):
#     with open(DATA_FILE, "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)


# @app.get("/punishments", response_model=List[Punishment])
# def get_punishments(category: Optional[str] = None):
#     data = load_data()
#     if category:
#         data = [p for p in data if p["category"] == category]
#     return data


# @app.get("/punishments/random", response_model=Punishment)
# def get_random_punishment(category: Optional[str] = None):
#     data = load_data()
#     if category:
#         data = [p for p in data if p["category"] == category]

#     if not data:
#         raise HTTPException(status_code=404, detail="No punishments found")

#     return random.choice(data)


# @app.post("/punishments", response_model=Punishment)
# def create_punishment(punishment: PunishmentCreate):
#     data = load_data()

#     new_id = max([p["id"] for p in data], default=0) + 1

#     new_punishment = {
#         "id": new_id,
#         "content": punishment.content,
#         "category": punishment.category,
#         "createdAt": datetime.utcnow().isoformat(),
#     }

#     data.append(new_punishment)
#     save_data(data)

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from fastapi.middleware.cors import CORSMiddleware
import random

from src.database import engine, Base, AsyncSessionLocal
from src.model import Punishment
from src.schemas import PunishmentCreate, PunishmentUpdate, PunishmentResponse

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://astrology-webapp-alpha.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB作成
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # 初期データ投入
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Punishment))
        existing = result.scalars().first()

        if not existing:
            print("初期データを投入します...")

            initial_data = [
                {"content": "変顔で写真を撮る", "category": "light"},
                {"content": "次の1杯をおごる", "category": "light"},
                {"content": "好きな人を暴露する", "category": "embarrassing"},
                {"content": "腕立て伏せ20回", "category": "physical"},
                {"content": "全力でモノマネする", "category": "embarrassing"},
            ]

            for item in initial_data:
                session.add(Punishment(**item))

            await session.commit()
            print("初期データ投入完了")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@app.post("/punishments", response_model=PunishmentResponse)
async def create_punishment(
    data: PunishmentCreate,
    db: AsyncSession = Depends(get_db)
):
    new_punishment = Punishment(
        content=data.content,
        category=data.category
    )
    db.add(new_punishment)
    await db.commit()
    await db.refresh(new_punishment)
    return new_punishment


@app.get("/punishments/random", response_model=PunishmentResponse)
async def get_random_punishment(
    category: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Punishment)
    if category:
        query = query.where(Punishment.category == category)

    result = await db.execute(query)
    punishments = result.scalars().all()

    if not punishments:
        return {"id": 0, "content": "データがありません", "category": "none"}

    return random.choice(punishments)

@app.post("/punishments/{punishment_id}/like")
async def like_punishment(
    punishment_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Punishment).where(Punishment.id == punishment_id)
    )
    punishment = result.scalar_one_or_none()

    if not punishment:
        return {"error": "Not found"}

    punishment.likes += 1
    await db.commit()
    await db.refresh(punishment)

    return punishment

@app.get("/punishments/popular", response_model=list[PunishmentResponse])
async def get_popular(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Punishment).order_by(Punishment.likes.desc())
    )
    return result.scalars().all()

@app.delete("/punishments/{punishment_id}")
async def delete_punishment(
    punishment_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Punishment).where(Punishment.id == punishment_id)
    )
    punishment = result.scalar_one_or_none()

    if not punishment:
        return {"error": "Not found"}

    await db.delete(punishment)
    await db.commit()

    return {"message": "Deleted"}

# mofify
@app.put("/punishments/{punishment_id}", response_model=PunishmentResponse)
async def update_punishment(
    punishment_id: int,
    data: PunishmentUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Punishment).where(Punishment.id == punishment_id)
    )
    punishment = result.scalar_one_or_none()

    if not punishment:
        return {"error": "Not found"}

    punishment.content = data.content
    punishment.category = data.category

    await db.commit()
    await db.refresh(punishment)

    return punishment