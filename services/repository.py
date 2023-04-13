from uuid import UUID
from sqlalchemy.orm import Session
from typing import Optional

from db.models import Prompt

class PromptRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, uuid: str) -> Prompt:
        prompt = Prompt(uuid=uuid)
        self.session.add(prompt)
        self.session.commit()
        self.session.refresh(prompt)
        return prompt

    def get_all(self) -> list:
        return self.session.query(Prompt).all()

    def get_by_id(self, prompt_id: int) -> Prompt:
        return self.session.query(Prompt).filter(Prompt.id == prompt_id).first()

    def get_by_uuid(self, uuid: str) -> Prompt:
        return self.session.query(Prompt).filter(Prompt.uuid == uuid).first()

    def update_by_uuid(self, uuid: UUID, call_id: Optional[str] = None, generated: Optional[bool] = False, text: Optional[str] = None) -> Prompt:
        prompt = self.session.query(Prompt).filter(Prompt.uuid == uuid).first()

        if prompt is None:
            return None

        if call_id is not None:
            prompt.call_id = call_id

        if generated is not False:
            prompt.generated = generated

        if text is not None:
            prompt.text = text

        self.session.commit()
        return prompt