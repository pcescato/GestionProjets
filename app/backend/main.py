from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Text, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from sentence_transformers import SentenceTransformer
import re
import os

app = FastAPI(title="Notes Backend avec Embeddings")

# Variables d'environnement pour la config
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://notesuser:notespwd@mariadb/notesdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(JSON)  # Stockage JSON du vecteur
    tags = Column(JSON)       # Liste de tags simples

Base.metadata.create_all(bind=engine)

model = SentenceTransformer('all-MiniLM-L6-v2')  # Modèle local léger

class NoteIn(BaseModel):
    content: str

class NoteOut(BaseModel):
    id: int
    tags: list[str]

def extract_tags(text: str, max_tags=5):
    stopwords = {"le", "la", "les", "de", "des", "un", "une", "et", "à", "en", "du"}
    words = re.findall(r'\b\w{4,}\b', text.lower())
    freq = {}
    for w in words:
        if w not in stopwords:
            freq[w] = freq.get(w, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in sorted_words[:max_tags]]

@app.post("/documents", response_model=NoteOut)
async def create_note(note_in: NoteIn):
    embedding = model.encode(note_in.content).tolist()
    tags = extract_tags(note_in.content)

    db = SessionLocal()
    note = Note(content=note_in.content, embedding=embedding, tags=tags)
    db.add(note)
    db.commit()
    db.refresh(note)
    db.close()

    return NoteOut(id=note.id, tags=tags)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
