#!/usr/bin/bash
dropdb trivia_test
createdb trivia_test
echo "DataBase trivia_test created."

psql trivia_test < trivia.psql
echo "trivia_test populated."

coverage run --source=. -m unittest test_flaskr.py
coverage report

