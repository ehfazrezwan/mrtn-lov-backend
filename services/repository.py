from db.models import Prompt
from sqlalchemy.orm import Session

class PromptRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, text: str) -> Prompt:
        prompt = Prompt(text=text)
        self.session.add(prompt)
        self.session.commit()
        self.session.refresh(prompt)
        return prompt

    def get_all(self) -> list:
        return self.session.query(Prompt).all()

    def get_by_id(self, prompt_id: int) -> Prompt:
        return self.session.query(Prompt).filter(Prompt.id == prompt_id).first()
