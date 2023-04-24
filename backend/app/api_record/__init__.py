#!/usr/bin/env python
# coding=utf-8

from flask import Blueprint

api_record = Blueprint('api_record', __name__)

from .api import *
from .errors import *
