from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from sentence_transformers import SentenceTransformer
import re

app = FastAPI(title="Backend Notes avec Embeddings")

DATABASE_URL = "mysql+pymysql://notesuser:notespwd@localhost/notesdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(JSON)  # Stocke liste float dans JSON
    tags = Column(JSON)       # Liste de tags simples

Base.metadata.create_all(bind=engine)

model = SentenceTransformer('all-MiniLM-L6-v2')  # modèle léger local

class NoteIn(BaseModel):
    content: str

class NoteOut(BaseModel):
    id: int
    tags: list[str]

def extract_tags(text: str, max_tags=5):
    # Extraction simple : mots fréquents >3 lettres, sans stopwords basiques
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