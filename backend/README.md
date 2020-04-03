# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment & Dependencies

You should install `pipenv` on your machine.

The following command installs the dependencies:

```bash
pipenv install
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

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
pipenv shell
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Endpoints

### /quizzes

#### POST

- Fetches a random question in a given category.
- Request body; quiz_category should be given:
```
{"quiz_category": {"id": 1, "type": "science"}}
```
- Returns: a random question in this category with the format:
```
  {"success": True, "question": {"id": 1, "question": "", "answer": "", category: 0, "difficulty": 1}}
```

### /questions

#### GET

- Fetches all questions
- Optional parameter: `page`, specifies the number of questions shown in one page. The default number is 10.
- Returns:

```
{
  "questions": [{
    "id": 0,
    "question": "",
    "answer": "",
    "category": 0,
    "difficulty": 0
  }],
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "total_questions": 12
  "success": true
}
```

#### POST

- Post a new question
- Request body:

```
{
    "question": "",
    "answer": "",
    "category": 0,
    "difficulty"; 0
}
```

- Returns:

```
{
    "success": True,
    "created": 20,
    "questions": [{
        "id": 0,
        "question": "",
        "answer": "",
        "category": 0,
        "difficulty": 0
  }],
}
```

### /questions/<question_id>

#### DELETE

- Delete a given question
- Parameter: `question_id`
- Returns:

```
{
    "success": True,
    "deleted": 20,
    "questions": [{
        "id": 0,
        "question": "",
        "answer": "",
        "category": 0,
        "difficulty": 0
  }],
}
```

### /categories

#### GET

- Get all categories
- Returns:

```
  {
      "categories": {
          "1": "Science",
          "2": "Art",
          "3": "Geography",
          "4": "History",
          "5": "Entertainment",
          "6": "Sports"
      },
      "success": true
  }
```

### /categories/<category_id>/questions

#### GET

- Get all questions for a given category
- Parameter: `category_id`
- Returns:

```
{
    "success": True,
    "questions": [{
        "id": 0,
        "question": "",
        "answer": "",
        "category": 0,
        "difficulty": 0
    }],
    "total_question": 20,
    "current_category": 2
}
```

### /search

#### POST

- Case insensitive search for questions containing the given string.
- Request body:

```
{
    "searchTerm": "what"
}
```

- Returns:

```
{
    "success": True,
    "questions": [{
        "id": 0,
        "question": "",
        "answer": "",
        "category": 0,
        "difficulty": 0
    }],
    "total_question": 20,
}
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
