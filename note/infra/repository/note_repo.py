from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from database.database import SessionLocal
from note.domain.note import Note as NoteV0
from note.domain.repository.note_repo import INoteRepository
from note.infra.db_models.note import Note, Tag
from utils.db_utils import row_to_dict

class NoteRepository(INoteRepository):
    def get_notes(
        self, 
        user_id: str,
        page: int,
        items_per_page: int,
        ) -> tuple[int, list[Note]]:
        with SessionLocal() as db: 
            query = (db.query(Note)
                     .options(joinedload(Note.tags))
                     .filter(Note.user_id == user_id))
            total_count = query.count()
            notes = (
                query.offset((page -1)* items_per_page)
                .limit(items_per_page).all()
            )

        note_vos = [NoteV0(**row_to_dict(note)) for note in notes]

        return total_count, note_vos
        
    
    def find_by_id(self, 
                   user_id: str,
                   id: str) -> Note:
        with SessionLocal() as db:
            note = (db.query(Note)).options(joinedload(Note.tags)).filter(Note.user_id ==user_id, Note.id == id).first()
            if not note: 
                raise HTTPException(status_code=422)
        
        return NoteV0(**row_to_dict(note))        
    
    def save(self, 
             user_id: str, 
             note_v0: NoteV0) -> Note:
        with SessionLocal() as db:
            tags: list[Tag] = []
            for tag in note_v0.tags:
                existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
                if existing_tag:
                    tags.append(existing_tag)
                else:
                    tags.append(
                        Tag(
                            id=tag.id, 
                            name=tag.name, 
                            created_at=tag.created_at, 
                            updated_at=tag.updated_at, 
                        )
                    )

            new_note = Note(
                id = note_v0.id, 
                user_id=user_id,
                title=note_v0.title, 
                content=note_v0.content, 
                memo_date=note_v0.memo_date, 
                tags=tags, 
                created_at=note_v0.created_at,
                updated_at=note_v0.updated_at,
            )
            db.add(new_note)
            db.commit()
    
    def update(self,
               user_id:str,
               note_v0: NoteV0) -> Note:
        with SessionLocal() as db:
            self.delete_tags(user_id, note_v0.id)

            note = (db.query(Note).filter(Note.user_id ==user_id, Note.id == note_v0.id).first())
            if not note: 
                raise HTTPException(status_code=422)
            
            note.title = note_v0.title
            note.content = note_v0.content
            note.memo_date = note_v0.memo_date

            tags: list[Tag] = []
            for tag in note_v0.tags:
                existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
                if existing_tag:
                    tags.append(existing_tag)
                else:
                    tags.append(
                        Tag(
                            id=tag.id, 
                            name=tag.name, 
                            created_at=tag.created_at, 
                            updated_at=tag.updated_at, 
                        )
                    )
            
            note.tags= tags
            db.add(note)
            db.commit()

            return NoteV0(**row_to_dict(note))
    
    def delete(self, 
               user_id: str,
               id: str):
        with SessionLocal() as db:
            self.delete_tags(user_id, id)

            note = db.query(Note).filter(Note.user_id == user_id, Note.id == id).first()
            if not note:
                raise HTTPException(status_code=422)
            
            db.delete(note)
            db.commit()
    
    def delete_tags(self, 
                    user_id: str,
                    id: str):
        with SessionLocal() as db: 
            note = db.query(Note).filter(Note.user_id == user_id, Note.id == id).first()
            if not note:
                raise HTTPException(status_code=422)
            
            note.tags=[]
            db.add(note)
            
            unused_tags = db.query(Tag).filter(~Tag.notes.any()).all()
            for tag in unused_tags:
                db.delete(tag)

            db.commit()
        
    
    def get_notes_by_tag_name(
        self, 
        user_id: str, 
        tag_name: str,
        page: int,
        items_per_page: int,
    ) -> tuple[int, list[Note]]:
        with SessionLocal() as db:
            tag = (db.query(Tag)
                   .filter_by(name=tag_name)
                   .first())

            if not tag: 
                return 0, []
            
            query= (db.query(Note)
                    # .option(joinedload(Note))
                    .filter(Note.user_id == user_id, 
                            Note.tags.any(id=tag.id),
                            )
                    )

            total_count = query.count()
            notes = (query.offset((page -1)* items_per_page)
                     .limit(items_per_page).all())

        note_vos = [NoteV0(**row_to_dict(note)) for note in notes]

        return total_count, note_vos
    
    