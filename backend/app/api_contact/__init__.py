"""
@Author: Wang Shenghe
@Date: 2023/4/30
"""

from flask import Blueprint

api_contact = Blueprint('api_contact', __name__)

from .api import *
from .errors import *
