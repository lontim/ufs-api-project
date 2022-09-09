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
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

