from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from .models import Base
from .schemas import NoteIn, NoteOut
from .database import get_db, engine
from ..services.notes import create_note, extract_tags

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/documents", response_model=NoteOut)
def create_note_route(note_in: NoteIn, db: Session = Depends(get_db)):
    note = create_note(db, note_in)
    return NoteOut(id=note.id, tags=note.tags)
