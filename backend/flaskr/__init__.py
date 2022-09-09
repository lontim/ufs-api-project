from http.client import OK
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    CORS(app, resources={"/api/*": {"origins": "*"}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, OPTION, DELETE"
        )
        response.headers.add(
            "Access-Control-Allow-Headers",
              "Content-Type" # ,Authorization
        )
        return response

    """
    Endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=["GET"])
    def get_categories():
        all_categories = Category.query.order_by(Category.id).all()
        category_dict = {}

        if len(all_categories) == 0:
            abort(404) # show an HTTP 404 or 204 no content response if no categories exist

        for single_category in all_categories:
            category_dict[single_category.id] = single_category.type

        return jsonify({"categories": category_dict})


    """
    Endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint returns a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions", methods=["GET"])
    def get_questions():
        all_questions = Question.query.order_by(Question.id).all()

        page_param = request.args.get("page", 1, type=int) # enabling pagination
        # if page_param <= 1:
        #            abort(404) # show an HTTP 404 or 204 if a page number below "one" was requested
        # the API assumes that the first page is "1" so need to factor this in to determine
        # the actual question identifiers within the range. So, set our real "page" as param - 1:
        page = page_param - 1
        first_question_id = (page) * QUESTIONS_PER_PAGE
        max_question_id = first_question_id + QUESTIONS_PER_PAGE

        all_question_list = []

        for single_question in all_questions:
            all_question_list.append(single_question.format())

        questions_subset_dict = all_question_list[first_question_id:max_question_id]

        if len(questions_subset_dict) == 0:
            abort(404)

        all_categories = Category.query.order_by(Category.id).all()
        category_dict = {}

        # if len(all_categories) == 0:
        #    abort(404) # show an HTTP 404 or 204 no content response if no categories exist

        for single_category in all_categories:
            category_dict[single_category.id] = single_category.type

        return jsonify(
            {
                "questions": questions_subset_dict,
                "totalQuestions": len(all_questions),
                "categories": category_dict,
                "currentCategory": None,
            }
        )

    """
    An endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<int:id>", methods=['DELETE'])
    def delete_question(id):
        question = Question.query.get(id)
        if not question:
            abort(404)
        try:
            question.delete()
        except:
            abort(422)
        return jsonify(
            {
                "success": True,
                "deleted": id,
            }
        )

    """
    GET endpoint to get questions based on category.
    """
    @app.route("/categories/<int:id>/questions",methods=["GET"])
    def get_questions_by_category(id):

        cat_questions = Question.query.filter_by(category=id).all()
        format_cat_questions = list() # start with an empty list of questions

        for question in cat_questions:
            format_cat_questions.append(question.format())

        cat = Category.query.get(id)

        return jsonify(
            {
                "questions": format_cat_questions,
                "totalQuestions": len(format_cat_questions),
                "currentCategory": cat.type,
            }
        )


    """
    POST a new question, which requires the question and answer text,
    category, and difficulty score.
    """

    @app.route("/questions", methods=["POST"])
    def add_question():
        request_data = request.get_json()
        try:
            question = Question(
                question=request_data.get("question"),
                answer=request_data.get("answer"),
                category=request_data.get("category"),
                difficulty=request_data.get("difficulty"),
            )
            question.insert()
            return jsonify({'success': True, 'created': question.id})
        except:
            abort(422)

    @app.route("/questions/search",methods=["POST"])
    def search_questions():
        search_term = request.get_json().get("searchTerm")
        # print('Reached the search route!', file=sys.stderr)
        questions_found = Question.query.filter(
            Question.question.ilike(f"%{search_term}%")
        )
        search_results = list()
        for question in questions_found:
            search_results.append(question.format())

        return jsonify(
            {
                "questions": search_results,
                "totalQuestions": len(search_results)
            }
        )


    # POST quizzes endpoint is used to play the quiz.
    # Takes an optional category and previous questions. Returns a random question
    # that wasn't already asked (within the optional category if specified).
    @app.route('/quizzes', methods=['POST'])
    def quiz():
        try:
            post_body = request.get_json()
            category = post_body.get('quiz_category') # category, if specified.
            previous_questions = post_body.get('previous_questions')
            if (category['id'] == 0):
                questions_filt = Question.query.all() # no category?
            else:
                questions_filt = Question.query.filter_by \
                        (category=category['id']). all()

            next_questions = list()
            for question in questions_filt:
                if question.id not in previous_questions:
                    next_questions.append(question)

            random_choice = random.randint(0, len(next_questions)-1)
            print (random_choice)

            nextQuestion = next_questions[random_choice]
            return (jsonify({"question": nextQuestion.format()}))
        except Exception:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "Not found"}), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return (
            jsonify(
                {"success": False, "error": 422, "message": "Unprocessable entity"}
            ),
            422,
        )


    return app

