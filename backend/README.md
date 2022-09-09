# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.


## Trivia API Reference

## 1. Get category endpoint

`GET /categories`

- Fetches a dictionary of categories.
  - Keys are IDs
  - Values are strings of each category

### 1.1 Example request using CURL
`curl http://localhost:5000/categories`

#### 1.2 Example response
```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports",
  "7": "Lunar Exploration"
}
```

## 2. Get questions endpoint

`GET /questions`

 - Fetches a page of questions (max 10 per page)
   - You may also provide an optional _**page**_ parameter - this comes in handy once your database of questions increases in size
   - If the page is not specified, the API assumes you want the first page
   - In the response, you'll receive
     - a list of questions
     - number of total questions
     - current category
     - categories

### 2.1 Example requests using CURL

* No _**page**_ specified:

```powershell
curl http://localhost:5000/questions
```

* Including the _**page**_ number parameter, we want to see "page two":

```powershell
curl http://localhost:5000/questions?page=2
```
  * The example response for the "page two" query is shown below.
---
**ℹ️ _N.B._**

> The pages in the trivia API questions endpoint begin at _**page 1**_. Requesting questions _**page zero**_, for example, would be considered an *invalid* request by the API, and would generate an error.

---
**ℹ️ _A time saving tip for applications building on the Trivia API_**

> You *don't* need to separately orchestrate calling the Category endpoint, when you're already calling the questions endpoint. You'll note that the trivia API already returns all of the trivia categories, alongside the set of questions.

---

#### 2.2 Question endpoint example response - "page two"
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "currentCategory": null, 
  "questions": [
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ], 
  "totalQuestions": 19
}
```

## 3. Delete questions endpoint

`DELETE /questions/<question_identifier>`

 - Deletes a question, if it exists.
 - This is keyed on the _**question_id**_ field, it's mandatory to include this.

### 3.1 Example requests using CURL
`curl -X DELETE http://localhost:5000/questions/14`

### 3.2 Example response
```json
{
  "deleted": 14, 
  "success": true
}
```
## 4. Create a new question
`POST /questions`

 - this endpoint requires the POST request to pass in:
   - the new _**question**_ &
   - _**answer**_ text,
   - the _**category**_, and
   - _**difficulty**_ score of the new question.


## 5. Search for questions
`POST /questions/search`

### 5.1 Example request
`curl `
### 5.2 Example response
```json
{
  "deleted": 14, 
  "success": true
}
```

## 6. Find questions by category
`GET /categories/{id}/questions`
### 6.1 Example request 
`curl `
### 6.2 Example response
```json
{
  "deleted": 14, 
  "success": true
}
```

## 7. Post a quiz result
`POST /quizzes`
### 7.1 Example request 
`curl `
### 7.2 Example response
```json
{
  "deleted": 14, 
  "success": true
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
