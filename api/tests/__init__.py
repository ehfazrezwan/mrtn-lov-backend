import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

from fastapi.testclient import TestClient
from main import app
from db.database import Base, engine
from unittest import TestCase


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = TestClient(app)
        Base.metadata.create_all(bind=engine)
    
    def tearDown(self):
        Base.metadata.drop_all(bind=engine)
