#!/bin/sh

source /opt/bin/activate
cd /opt/tkv

./manage.py extract start tk_questions
./manage.py extract start tk_answers

sleep 300

./manage.py extract start tk_qa_matcher
