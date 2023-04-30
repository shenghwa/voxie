#!/usr/bin/env python
# coding=utf-8
import random

from app import db
from flask import request, jsonify, current_app, session
from flask.views import MethodView
from ..api_user.models import User
from .models import Record
from . import api_record


class RecordStoreAPI(MethodView):
    """
    Record store API
    """

    def post(self):
        """
        Store the record
        swagger_from_file: app/api_record/docs/add_record.yml
        """
        ret_json = {
            "status": 200,
            "message": "Store record successfully!",
            "request": request.base_url,
            "data": {}
        }

        token = request.values.get('token')
        user_id = User.confirm(token).get('id')
        content = request.values.get('content')

        record = Record()
        record.user_id = user_id
        record.content = content

        try:
            db.session.add(record)
            db.session.commit()
            return jsonify(ret_json)
        except:
            ret_json.update({
                "status": 500,
                "message": "Store records fail!"
            })
            db.session.rollback()
            return jsonify(ret_json)


class RecordListAPI(MethodView):
    """
    Get all the records from the login user by page API
    """

    def get(self):
        """
        Get record List.
        swagger_from_file: app/api_record/docs/record_get_list.yml
        """
        ret_json = {
            "status": 200,
            "message": 'Get the records successfully',
            "request": request.base_url,
            "data": {}
        }

        token = request.values.get('token')
        page = request.values.get("page") or 1
        number = request.values.get("number") or 20

        user_id = User.confirm(token).get('id')

        records_page = Record.query.filter_by(user_id=user_id).paginate(int(page), int(number))

        records_list = []
        if records_page:
            for record in records_page.items:
                records_dict = {}
                records_dict["content"] = record.content
                records_dict["update_time"] = record.update_time
                records_list.append(records_dict)
            ret_json.update({"data": {
                "items": records_list, "has_prev": records_page.has_prev,
                "has_next": records_page.has_next, "total_page": records_page.pages,
                "list_size": len(records_list)}}
            )

        return jsonify(ret_json)


class RecordDeleteAPI(MethodView):
    """
        Delete single record API
    """

    def delete(self):
        """
        Delete one record.
        swagger_from_file: app/api_record/docs/delete_record.yml
        """
        ret_json = {
            "status": 200,
            "message": 'Delete the record successfully',
            "request": request.base_url,
        }
        token = request.values.get('token')
        user_id = User.confirm(token).get('id')
        record_id = request.values.get('record_id')
        record = Record.query.filter_by(id=record_id, user_id=user_id).first()
        try:
            db.session.delete(record)
            db.session.commit()
            return jsonify(ret_json)
        except:
            db.session.rollback()
            ret_json.update({'status': 500, 'message': 'Failed!'})
            return jsonify(ret_json)


class RecordRecommendAPI(MethodView):
    """
    Get some recommended records API
    """

    def get(self):
        """
        Get some recommended records.
        swagger_from_file: app/api_record/docs/record_recommend.yml
        """
        ret_json = {
            "status": 200,
            "message": 'Get the questions successfully',
            "request": request.base_url,
            "data": {}
        }

        recommended_records = Record.query.all()
        len_records = len(recommended_records)
        recommended_index = []
        for i in range(7):
            r = random.randint(0, len_records - 1)
            if r not in recommended_index:
                recommended_index.append(r)
        recommended_list = [recommended_records[i].content.split('\n')[0] for i in recommended_index]
        ret_json.update({'data': {'recommend_questions': recommended_list}})
        print(ret_json)

        return jsonify(ret_json)


api_record.add_url_rule('/add', view_func=RecordStoreAPI.as_view('add'))
api_record.add_url_rule('/record_list', view_func=RecordListAPI.as_view('record_list'))
api_record.add_url_rule('/delete_record', view_func=RecordDeleteAPI.as_view('delete_record'))
api_record.add_url_rule('/recommended_question', view_func=RecordRecommendAPI.as_view('recommended_question'))

