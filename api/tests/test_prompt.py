import unittest
from unittest.mock import patch, Mock

import asyncio

from fastapi import HTTPException

from api.prompt import create_prompt, PromptInput
from services.google_sheets import GoogleSheets
from services.repository import PromptRepository

class TestPrompt(unittest.TestCase):
    @patch.object(GoogleSheets, 'append_row', return_value=None)
    @patch.object(PromptRepository, 'create', return_value=Mock(id=1))
    def test_create_prompt_success(self, mock_create, mock_append_row):
        response = asyncio.run(create_prompt(PromptInput(prompt='test prompt')))

        self.assertEqual(response, {"message": "Prompt created successfully"})
        mock_create.assert_called_once_with('test prompt')
        mock_append_row.assert_called_once()

    @patch.object(GoogleSheets, 'append_row', side_effect=Exception('Failed to append row'))
    @patch.object(PromptRepository, 'create', return_value=Mock(id=1))
    def test_create_prompt_google_sheets_failure(self, mock_create, mock_append_row):
        with self.assertRaises(HTTPException) as ex:
            asyncio.run(create_prompt(PromptInput(prompt='test prompt')))

        self.assertEqual(ex.exception.status_code, 500)
        self.assertEqual(str(ex.exception.detail), 'Failed to append row')
        mock_create.assert_called_once_with('test prompt')
        mock_append_row.assert_called_once()

    @patch.object(GoogleSheets, 'append_row', return_value=None)
    @patch.object(PromptRepository, 'create', side_effect=Exception('Database connection error'))
    def test_create_prompt_database_failure(self, mock_create, mock_append_row):
        with self.assertRaises(HTTPException) as ex:
            asyncio.run(create_prompt(PromptInput(prompt='test prompt')))

        self.assertEqual(ex.exception.status_code, 500)
        self.assertEqual(str(ex.exception.detail), 'Database connection error')
        mock_create.assert_called_once_with('test prompt')
        mock_append_row.assert_not_called()
