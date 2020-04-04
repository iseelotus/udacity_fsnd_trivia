import os
from flask import Flask, request, abort, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from werkzeug.exceptions import HTTPException

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r'/*': {'origins': '*'}})
  
  current_category = Category.query.first().format()
  
  # CORS Header
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/categories')
  def retrieve_categories():
    categories = get_categories()
    return jsonify({
      'success': True,
      'categories': categories
    })

  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
    all_questions = Question.query.order_by(Question.id).all()
    categories = get_categories()
    current_questions = paginate_questions(request, all_questions)

    if len(current_questions)==0:
      abort(404)
    else:
      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(all_questions),
        'categories': categories,
        'current_category': current_category
      })

  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)

      if question is None:
        abort(404)
      else:
        question.delete()
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions': current_questions
      })
    except:
      abort(422)

  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    try:
      question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions
      }), 201

    except:
      abort(422)

  @app.route('/search', methods=['POST'])
  def search():
    search_term = request.json.get('searchTerm', '')
    questions = [question.format() for question in Question.query.filter(Question.question.ilike(f'%{search_term}%')).order_by(Question.id).all()]
    return jsonify({
      'sucess': True,
      'questions': questions,
      'total_questions': len(questions)
    })
  
  @app.route('/categories/<int:category_id>/questions')
  def retrieve_questions_by_category(category_id):
    questions = [question.format() for question in Question.query.filter(Question.category==category_id)]
    if len(questions) == 0:
      return abort(404)
    else:
      return jsonify({
        'success': True,
        'questions': questions,
        'total_question': len(questions),
        'current_category': category_id
      })


  @app.route('/quizzes', methods=['POST'])
  def retrieve_quiz_question():
    body = request.get_json()
    category = body.get('quiz_category')

    if (category['id'] == 0):
      questions = Question.query.all()
    else:
      questions = Question.query.filter_by(category=category['id']).all()
    
    return jsonify({
      'success': True,
      'question': questions[random.randrange(0, len(questions), 1)].format()
    })
  
  @app.errorhandler(HTTPException)
  def http_exception_handler(error):
    return jsonify({
      'success': False,
      'error': error.code,
      'message': error.description
    }), error.code

  return app

def paginate_questions(request, all_questions):
  page = request.args.get('page', 1, type=int)
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in all_questions]
  current_questions = questions[start:end]
  return current_questions

def get_categories():
  categories = {}
  for category in Category.query.all():
    categories[category.id] = category.type
  return categories
