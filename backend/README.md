# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 
```

### Endpoints

| Method &nbsp; &nbsp; |    Syntax   |
| :----- | :----- |
| GET   | '/categories' |
| GET   | '/categories/\<int:category_id>/questions?page=<page_number>' |
| GET   | '/questions?page=<page_number>' |
| DELETE| '/questions/\<int:question_id>' |
| POST  | '/categories/\<int:category_id>/questions' |
| POST  | '/questions' |
| POST  | '/quizzes' |


#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Response: 
  + A completed request will return a **200** status code, and then return a json object.
  Example:
  ```javascript
  {
    "categories": {
      "1": "Science", 
      "2": "Art", 
      "3": "Geography", 
      "4": "History", 
      "5": "Entertainment", 
      "6": "Sports"
    }, 
    "success": true, 
    "total_categories": 6
  }
  ``` 
  + If no category was found, the request will return a **404** status code.

#### GET '/categories/<int:category_id>/questions?page=<page_number>'
- Fetches questions within a specified category.
- Request Arguments: **category_id**
- Response: 
  + A completed request will return a **200** status code. Example json object for return:
  ```javascript
  {
    "currentCategory": 1, 
    "questions": [
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
      }
    ], 
    "success": true, 
    "totalQuestions": 3
  }
  ``` 

#### GET '/questions?page=<page_number>'
- Fetches questions on a page (10 questions per page).
- Request Arguments: None
- Response: 
  + A completed request will return a **200** status code. Example json object for return:
  ```javascript
  {
    "categories": {
      "1": "Science", 
      "2": "Art", 
      "3": "Geography", 
      "4": "History", 
      "5": "Entertainment", 
      "6": "Sports"
    }, 
    "current_category": 5, 
    "questions": [
      {
        "answer": "Tom Cruise", 
        "category": 5, 
        "difficulty": 4, 
        "id": 4, 
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      }, 
      {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }, 
      {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }, 
      {
        "answer": "Uruguay", 
        "category": 6, 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }, 
      {
        "answer": "George Washington Carver", 
        "category": 4, 
        "difficulty": 2, 
        "id": 12, 
        "question": "Who invented Peanut Butter?"
      }, 
      {
        "answer": "Lake Victoria", 
        "category": 3, 
        "difficulty": 2, 
        "id": 13, 
        "question": "What is the largest lake in Africa?"
      }, 
      {
        "answer": "The Palace of Versailles", 
        "category": 3, 
        "difficulty": 3, 
        "id": 14, 
        "question": "In which royal palace would you find the Hall of Mirrors?"
      }, 
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
      }
    ], 
    "success": true, 
    "total_questions": 17
  }
  ``` 

#### DELETE '/questions/<int:question_id>'
- Delete a question with specified question_id.
- Request Arguments: **question_id**
- Response: 
  + A completed request will return a **200** status code. Example json object for return:
  ```javascript
  {
    "deleted": 2,
    "success": true
  }
  ```
  + If the question_id is not found, will return a **404** status code.

#### POST '/categories/<int:category_id>/questions'
- Post a new question along with answer, category and difficulty socre.
- Request Argument: **category_id**
- Required entries within request body:
  + question, str
  + answer, str
  + difficulty, int
  + category id, int
- Response: 
  + A completed request will return a **200** status code. Example json object for return:
  ```javascript
  { "success": true }
  ```
  + Upon failed creation, will return a **422** status code.

#### POST '/questions'
- Fetches questions on a page (10 questions per page) based on a search term.
- Request Arguments: None
- Request body:
  + searchTerm, str
- Response: 
  + A completed request will return a **200** status code. Example json object for return:
  ```javascript
  {
    "currentCategory": 5, 
    "questions": [
      {
        "answer": "Tom Cruise", 
        "category": 5, 
        "difficulty": 4, 
        "id": 4, 
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      }, 
      {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }, 
      {
        "answer": "Lake Victoria", 
        "category": 3, 
        "difficulty": 2, 
        "id": 13, 
        "question": "What is the largest lake in Africa?"
      }, 
      {
        "answer": "Mona Lisa", 
        "category": 2, 
        "difficulty": 3, 
        "id": 17, 
        "question": "La Giaconda is better known as what?"
      }, 
      {
        "answer": "The Liver", 
        "category": 1, 
        "difficulty": 4, 
        "id": 20, 
        "question": "What is the heaviest organ in the human body?"
      }, 
      {
        "answer": "Blood", 
        "category": 1, 
        "difficulty": 4, 
        "id": 22, 
        "question": "Hematology is a branch of medicine involving the study of what?"
      }, 
      {
        "answer": "1/2", 
        "category": 2, 
        "difficulty": 3, 
        "id": 24, 
        "question": "What is the spin number of a electron?"
      }
    ], 
    "success": true, 
    "totalQuestions": 7
  }
  ```


#### POST '/quizzes'
- Fetches questions to play the quiz. This endpoint will take category and previous question parameters and return a random questions within the given category, if provided. The returned question will not be one of the previous questions.
- Request Arguments: None
- Request Body:
  quiz_category, int
  previous_questions, list of int
- Response: 
  + A completed request will return a **200** status code. Example json object for return:
  ```javascript
  {
    "question": {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    "success": true
  }
  ```
  + Upon failed creation, will return a **422** status code.

## Testing
To run the tests, execute the script below:
```bash
./test_trivia.sh
```