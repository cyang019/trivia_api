#!/usr/bin/bash
coverage run --source=. -m unittest backend/test_flaskr.py
coverage report

