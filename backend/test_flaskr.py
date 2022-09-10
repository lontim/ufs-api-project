import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from settings import DB_NAME, DB_USER, DB_PASSWORD

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name) # "sql" here after "postgres" stops the "dialect name" warning
        setup_db(self.app, self.database_path)

        self.question_to_add = {
            "question": "How many stars in our galaxy, the Milky Way?",
            "answer": "100 thousand million stars",
            "difficulty": 3,
            "category": 1
        }

        self.question_incomplete = {
            "answer": "100 thousand million stars",
            "category": 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after each test"""
        pass

    def test_category(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)        
        self.assertEqual(res.status_code,200)

    def test_category_fail(self):
        # try to use delete HTTP method - expect a 405 HTTP error
        res = self.client().delete("/categories")
        self.assertEqual(res.status_code,405)

    def test_question_happy(self):
        res = self.client().get("/questions?page=2")
        data = json.loads(res.data)        
        self.assertEqual(res.status_code,200)
        # tries to load page 2 of questions - should succeed with 200

    def test_question_fail_high_pagination(self):
        res = self.client().get("/questions/7")
        self.assertEqual(res.status_code,405)
        # this tries to load a non-existant page of questions - expect 405

    def test_question_create(self):
        res = self.client().post("/questions", json=self.question_to_add)
        self.assertEqual(res.status_code,200)

    def test_question_create_fail(self):
        res = self.client().post("/questions", json=self.question_incomplete)
        self.assertEqual(res.status_code,200)

    def test_question_delete(self):
        res = self.client().post("/questions", json=self.question_to_add)
        data = json.loads(res.data)
        added_id = data["created"]
        res = self.client().delete("/questions/{}".format(added_id))
        self.assertEqual(res.status_code, 200)

    def test_question_delete_fail(self):
        # try to delete an invalid question ID
        res = self.client().delete("/questions/7766")
        # expect to see a 404 Not Found
        self.assertEqual(res.status_code, 404)

    def test_question_search(self):
        # try searching for something we know is in a question
        search_payload = {"searchTerm": "graph"}
        res = self.client().post("/questions/search", json=search_payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["questions"]), 2)

    def test_question_search_failure(self):
        # try searching for something that isn't in any questions
        search_payload = {"searchTerm": "null"}
        res = self.client().post("/questions/search", json=search_payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["questions"]), 0)

    def test_simulate_quiz_happy(self):
        self.get_next_question = {
            "previous_questions": [13, 14],
            "quiz_category": {"type": "Geography", "id": "3"},
        }
        # We assume that the user has chosen Geography topic;
        # last two questions are specified. Check correct question
        # that was not yet asked, is returned.
        res = self.client().post("/quizzes", json=self.get_next_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["question"].get("id"), 15)

    def test_simulate_quiz_unhappy(self):
        self.get_next_question = {
            "previous_questions": [13, 14, 15],
            "quiz_category": {"type": "Geography", "id": "3"},
        }
        # We assume that the user has chosen Geography topic;
        # last three questions are specified. 
        # Check that quiz ends.
        res = self.client().post("/quizzes", json=self.get_next_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["forceEnd"], "true")
        
    def test_question_search_unhappy(self):
        search_payload = {"searchTerm": "xyzxyz"}
        res = self.client().post("/questions/search", json=search_payload)
        data = json.loads(res.data)

        # confirm that no questions are returned, when incorrect search term provided:
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["questions"]), 0)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
