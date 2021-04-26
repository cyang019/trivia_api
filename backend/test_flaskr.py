import sys
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
sys.path.insert(0, os.path.dirname(__file__))
from flaskr import create_app, QUESTIONS_PER_PAGE
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def _get_res_data(self, method='get', route=''):
        op = getattr(self.client(), method, None)
        if callable(op):
            res = op(route)
            data = json.loads(res.data)
            return data
        else:
            raise NotImplementedError
    """
    TODO
    Write at least one test for each test for successful
    operation and for expected errors.
    """
    def test_retrieve_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['questions']) <= QUESTIONS_PER_PAGE)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['current_category'])
        self.assertTrue(data['total_questions'])

    def test_404_get_questions_page_number_beyond_valid(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['error'], 404)

    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)

    def test_404_delete_none_existing_question(self):
        res = self.client().delete('/questions/999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['error'], 404)

    def test_create_question(self):
        res = self.client().post(
            'categories/1/questions',
            json={
                "question": "Is electron a fermion or a boson?",
                "answer": "It's a fermion.",
                "difficulty": 3
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_question(self):
        res = self.client().post(
            'categories/2/questions',
            json={
                'question': 'haha..',
                'answer': 'what?'
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')

    def test_search_question(self):
        res = self.client().post(
            '/questions',
            json={
                'searchTerm': 'what'
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['currentCategory'])
        self.assertTrue(data['totalQuestions'])

    def test_search_category_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['currentCategory'])

    def test_next_quiz_question(self):
        res = self.client().post('/quizzes', json={
            "quiz_category": {"id": 1, "type": "Science"},
            "previous_questions": [20]
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']['id'])

    def test_next_quiz_question_no_previous(self):
        res = self.client().post('/quizzes', json={
            "quiz_category": {"id": 2, "type": "Art"}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']['id'])

    def test_422_next_quiz_non_existing_category(self):
        res = self.client().post('/quizzes', json={
            "previous_questions": [20, 21]
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        self.assertEqual(data['error'], 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
