#!/usr/bin/bash
dropdb trivia_test
createdb trivia_test
echo "DataBase trivia_test created."

psql trivia_test < backend/trivia.psql
echo "trivia_test populated."

coverage run --source=. -m unittest backend/test_flaskr.py
coverage report

