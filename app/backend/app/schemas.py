from pydantic import BaseModel

class NoteIn(BaseModel):
    content: str

class NoteOut(BaseModel):
    id: int
    tags: list[str]
