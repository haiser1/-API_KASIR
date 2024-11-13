from base import base_response
from config import db
from flask import jsonify

db = db
jsonify = jsonify

base_response = base_response.BaseResponse()

