import uuid
import weaviate
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from ..models import Note
from ..schemas import NoteIn

model = SentenceTransformer('all-MiniLM-L6-v2')
weaviate_client = weaviate.Client("http://weaviate:8080")

def extract_tags(text: str, max_tags=5):
    import re
    stopwords = {"le", "la", "les", "de", "des", "un", "une", "et", "à", "en", "du"}
    words = re.findall(r'\b\w{4,}\b', text.lower())
    freq = {}
    for w in words:
        if w not in stopwords:
            freq[w] = freq.get(w, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in sorted_words[:max_tags]]

def create_note(db: Session, note_in: NoteIn):
    # 1. Embedding
    embedding = model.encode(note_in.content).tolist()
    tags = extract_tags(note_in.content)

    # 2. SQL
    note = Note(content=note_in.content, embedding=embedding, tags=tags)
    db.add(note)
    db.commit()
    db.refresh(note)

    # 3. Weaviate
    weaviate_client.data_object.create(
        data_object={"content": note_in.content, "tags": tags},
        class_name="Note",
        vector=embedding,
        uuid=str(uuid.uuid4())
    )

    return note
