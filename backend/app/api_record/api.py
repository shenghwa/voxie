#!/usr/bin/env python
# coding=utf-8

from app import db
from flask import request, jsonify, current_app
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


api_record.add_url_rule('/add', view_func=RecordStoreAPI.as_view('add'))
