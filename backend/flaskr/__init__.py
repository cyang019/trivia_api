import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [item.format() for item in selection]
  current_questions = questions[start:end]
  total_questions_count = len(questions)
  return current_questions, total_questions_count


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def retrieve_categories():
    selections = Category.query.order_by(Category.id).all()
    categories = [selection.format() for selection in selections]

    db.session.close()
    
    if len(categories) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'categories': categories,
      'total_categories': len(categories)
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions, total_questions_count = paginate_questions(request, selection)
    
    if len(current_questions) == 0:
      abort(404)

    category_selection = Category.query.order_by(Category.id).all()
    categories = [category.format() for category in category_selection]
    current_category = Category.query.get(current_questions[0]['category']).format()

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': total_questions_count,
      'categories': categories,
      'current_category': current_questions[0]['category']
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()
    if question is None:
      abort(404)
    
    question.delete()
    return jsonify({
      'success': True,
      'deleted': question_id
    })

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['POST'])
  def create_question(category_id):
    body = request.get_json()
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficulty = body.get('difficulty', None)
    new_category = category_id

    error = False
    try:
      if new_difficulty is None:
        raise ValueError(f'Need difficulty for the question, saw None.')
      category = Category.query.get(category_id)
      if category is None:
        category = Category(type=new_category)
        db.session.add(category)
        
      question = Question(question=new_question, answer=new_answer,
      category=category.id, difficulty=new_difficulty)
      question.insert()
      db.session.commit()
    except Exception as e:
      error = True
      print(f'error creating new question: {e}')
      db.session.rollback()
    finally:
      db.session.close()

    if error:
      abort(422)

    return jsonify({
      'success': True
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def search_question():
    body = request.get_json()
    search_term = body.get('searchTerm', '')
    questions = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_term)))
    current_questions, total_cnt = paginate_questions(request, questions)
    current_category = Category.query.get(current_questions[0]['id']).format()
    return jsonify({
      'success': True,
      'questions': current_questions,
      'totalQuestions': total_cnt,
      'currentCategory': current_category
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def retrieve_category_questions(category_id):
    selection = Question.query.filter(Question.category == category_id)
    current_questions, count = paginate_questions(request, selection)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'totalQuestions': count,
      'currentCategory': category_id
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def retrieve_next_question():
    body = request.get_json()
    quiz_category = body.get('quiz_category', None)
    if quiz_category is None:
      abort(422)
    previous_question_ids = body.get('previous_questions', None)
    if previous_question_ids is None:
      previous_question_ids = []
    
    questions = Question.query.filter(
      Question.category==quiz_category,
      ~Question.id.in_(previous_question_ids)
    ).all()
    question = None
    if len(questions) > 0:
      choice = random.choice(questions)
      question = choice.format()

    return jsonify({
      'success': True,
      'question': question
    })
    

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
  
  return app

    