#!/usr/bin/env python
# coding=utf-8

from app import db
from flask import request, jsonify, current_app, session
from flask.views import MethodView
from ..api_user.models import User
from . import api_contact


class ContactAnswerAPI(MethodView):
    """
    Get the answers from the common questions API
    """

    def get(self):
        """
        Get the answers from the selected question.
        swagger_from_file: app/api_contact/docs/contact_answer.yml
        """
        ret_json = {
            "status": 200,
            "message": 'Get the records successfully',
            "request": request.base_url,
            "data": {}
        }

        question_index = request.values.get('question_index')

        if question_index == '0':
            ret_json.update({'data': {'answer': 'Voxie is a smart voice interaction assistant, you can ask questions to'
                                                ' get answers. \n After signing up and signing in your account, then '
                                                'you can access to Voxie. '}})  # question0: Getting Start with Voxie
        elif question_index == '1':
            ret_json.update({'data': {'answer': 'Because the access is full, we need to limit the number of visits. '
                                                'If you want to ask more questions every day, you can upgrade to '
                                                'membership for premium services.'}})  # question1: Why can I only ask 15 questions a day?
        elif question_index == '2':
            ret_json.update({'data': {'answer': 'Voxie used a variety of corpora for training, involving many fields, '
                                                'such as engineering, computer, literature, history, etc.'}})  # question2: Which kind of questions can I ask?
        elif question_index == '3':
            ret_json.update({'data': {'answer': 'Because the training time and content is limited, can not cover '
                                                'everything in the world, but he can answer the common questions.'}})  # question3: Why can't I get answers to some questions?
        elif question_index == '4':
            ret_json.update({'data': {'answer': 'You can only sign up once with one email address due to the '
                                                'limitation'}})  # question4: Precautions for registration
        else:
            ret_json.update({'data': {'answer': 'I can\'t understand your question at the moment, I\'ll write it down '
                                                'and report back. If you are in hurry, please contact the human '
                                                'service'}})

        return jsonify(ret_json)


api_contact.add_url_rule('/answer', view_func=ContactAnswerAPI.as_view('answer'))

