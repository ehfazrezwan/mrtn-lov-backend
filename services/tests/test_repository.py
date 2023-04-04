from sqlalchemy.orm import Session
from services.repository import PromptRepository
from db.database import Base, engine
from unittest import TestCase


class TestPromptRepository(TestCase):
    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.db = Session(bind=engine)
        self.repo = PromptRepository(self.db)

    def tearDown(self):
        Base.metadata.drop_all(bind=engine)

    def test_create(self):
        prompt = self.repo.create("test prompt")
        self.assertEqual(prompt.text, "test prompt")

    def test_get_all(self):
        self.repo.create("test prompt 1")
        self.repo.create("test prompt 2")
        prompts = self.repo.get_all()
        self.assertEqual(len(prompts), 2)
        self.assertEqual(prompts[0].text, "test prompt 1")
        self.assertEqual(prompts[1].text, "test prompt 2")

    def test_get_by_id(self):
        prompt = self.repo.create("test prompt")
        retrieved_prompt = self.repo.get_by_id(prompt.id)
        self.assertEqual(retrieved_prompt.text, "test prompt")
