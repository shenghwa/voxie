#!/usr/bin/env python
# coding=utf-8

from app import db
from flask import request, jsonify, current_app
from flask.views import MethodView
from .models import User, Role
from .utils import confirm_token, confirm_key, Status
from . import api_user


class UserLoginAPI(MethodView):
    """
    login API
    """

    @confirm_key(["username", "password"])
    def post(self):
        """
        User login.
        swagger_from_file: app/api_user/docs/user_login.yml
        """
        ret_json = {
            "status": Status.SUCCESS.status,
            "message": "login success!",
            "request": request.base_url,
            "data": {
                "token": "",
            }
        }
        username = request.values.get("username")
        password = request.values.get("password")
        user = User.query.filter_by(username=username).first()
        if user and password:
            ret = user.verify_password(password)
            if ret:
                token = user.generate_confirmation_token()
                ret_json.update({"data": {"token": token}})
                return jsonify(ret_json)

        ret_json.update({
            "status": Status.FAIL.status,
            "message": "login fail!"
        })
        return jsonify(ret_json)


class UserLogoutAPI(MethodView):
    """
    logout API
    """

    def get(self):
        """
        User logout.
        # swagger_from_file: app/api_user/docs/user_logout.yml
        """
        return self.post()

    def post(self):
        """
        User logout.
        swagger_from_file: app/api_user/docs/user_logout.yml
        """
        ret_json = {
            "status": Status.SUCCESS.status,
            "message": "logout!",
            "request": request.base_url,
            "data": {}
        }
        return jsonify(ret_json)


class UserConfirmTokenAPI(MethodView):
    """
    Validate Token API
    """

    def get(self):
        return self.post()

    @confirm_token()
    def post(self):
        """
        Confirm token.
        swagger_from_file: app/api_user/docs/confirm_token.yml
        """

        ret_json = {
            "status": Status.SUCCESS.status,
            "message": Status.SUCCESS.message,
            "request": request.base_url,
            "data": {}
        }
        return jsonify(ret_json)


class UserInfoAPI(MethodView):
    """
    USER info API
    """

    @confirm_token()
    def get(self):
        """
        获取用户信息
        swagger_from_file: app/api_user/docs/user_get_info.yml
        """
        ret_json = {
            "status": Status.SUCCESS.status,
            "message": Status.SUCCESS.message,
            "request": request.base_url,
            "data": {}
        }

        token = request.values.get("token")
        if token:
            token_data = User.confirm(token)
            user_id = token_data.get('id')
            username = token_data.get("username")
            roles = token_data.get("roles")
            ret_json["data"].update({
                'id': user_id,
                "username": username,
                "roles": roles
            })
            return jsonify(ret_json)

        ret_json.update({
            "status": Status.FAIL.status,
            "message": "Get user informations fail!"
        })
        return jsonify(ret_json)


class UserChangePasswordAPI(MethodView):
    """
    Change password API
    """

    @confirm_key(["token", "password", "newpassword"])
    # @confirm_token
    def post(self):
        """
        Change user password.
        swagger_from_file: app/api_user/docs/user_change_password.yml
        """
        ret_json = {
            "status": Status.SUCCESS.status,
            "message": "change password successful!",
            "request": request.base_url,
            "data": {}
        }
        token = request.values.get("token")
        password = request.values.get("password")
        newpassword = request.values.get("newpassword")

        token_data = User.confirm(token)  # valid Token
        if token_data:
            user_id = token_data.get("id")
            user = User.query.get(user_id)
            if user and password:
                ret = user.verify_password(password)
                if ret:
                    user.password = newpassword
                    db.session.add(user)
                    db.session.commit()
                    return jsonify(ret_json)

        ret_json.update({
            "status": Status.FAIL.status,
            "message": "change password fail!"
        })
        return jsonify(ret_json)


class UserListAPI(MethodView):
    """
    get user info by page API
    """

    @confirm_token(["admin"])
    def get(self):
        """
        Get User List.
        swagger_from_file: app/api_user/docs/user_get_list.yml
        """
        ret_json = {
            "status": Status.SUCCESS.status,
            "message": Status.SUCCESS.message,
            "request": request.base_url,
            "data": {}
        }

        page = request.values.get("page") or 1
        number = request.values.get("number") or 20

        # print(page, number)
        users_page = User.query.paginate(int(page), int(number))

        user_lst = []
        if users_page:
            for user in users_page.items:
                u = {}
                u["id"] = user.id
                u["username"] = user.username
                u["roles"] = [role.name for role in user.roles]
                user_lst.append(u)
            ret_json.update({"data": {
                "items": user_lst, "has_prev": users_page.has_prev,
                "has_next": users_page.has_next, "total_page": users_page.pages,
                "lst_size": len(user_lst)}}
            )

        return jsonify(ret_json)


class UserRegisterAPI(MethodView):
    """
    register API
    """

    @staticmethod
    def create_role(name='normal'):
        """create Role"""

        # check if the role exists
        normal = Role.query.filter_by(name=name).first()
        # if not then create
        if not normal:
            normal = Role()
            normal.name = name
            db.session.add(normal)
            db.session.commit()
            print("The '%s' role is created!" % name)
        return normal


    @confirm_key(["username", "password", "email"])
    def post(self):
        """
        register.
        swagger_from_file: app/api_user/docs/user_register.yml
        """
        ret_json = {
            "status": Status.SUCCESS.status,
            "message": "Register Successful!",
            "request": request.base_url,
            "data": {}
        }

        normal = UserRegisterAPI.create_role()
        username = request.values.get("username")
        password = request.values.get("password")
        email = request.values.get("email")
        user = User()
        user.username = username
        user.password = password
        user.email = email
        user.roles = [normal]

        try:
            db.session.add(user)
            db.session.commit()
            return jsonify(ret_json)
        except:
            ret_json.update({
                "status": Status.FAIL.status,
                "message": "change password fail!"
            })
            db.session.rollback()
            return jsonify(ret_json)


api_user.add_url_rule('/login', view_func=UserLoginAPI.as_view('login'))
api_user.add_url_rule('/logout', view_func=UserLogoutAPI.as_view('logout'))
api_user.add_url_rule('/register', view_func=UserRegisterAPI.as_view('register'))
api_user.add_url_rule(
    '/confirm_token', view_func=UserConfirmTokenAPI.as_view('confirm_token'))
api_user.add_url_rule(
    '/info', view_func=UserInfoAPI.as_view('user_info'))
api_user.add_url_rule(
    '/change_password', view_func=UserChangePasswordAPI.as_view('change_password'))
api_user.add_url_rule(
    '/list', view_func=UserListAPI.as_view('user_list'))
