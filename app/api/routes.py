# from app import db
from app.models import Tire
from flask import current_app as app
from flask import jsonify, request, url_for, g
from sqlalchemy import and_
from app.api import bp
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
from app import db
from app.models import User
from flask_restful import Resource, abort
from flask_restful import reqparse
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
# from app import parser



def abort_if_param_doesnt_exist(t_id):
    if t_id not in ['diametr', 'width', 'height', 'count']:
        abort(404, message="Parameter {} do not exist.".format(t_id))

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


# @app.route('/api/resource')
class GetResource(Resource):
    @auth.login_required
    def get(self):
        return jsonify({ 'data': 'Hello, %s!' % g.user.username })

# @app.route('/api/token')
class GetAuthToken(Resource):
    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token(600)
        return jsonify({'token': token, 'duration': 600})

# @app.route('/api/users', methods = ['POST'])
class NewUser(Resource):
    def post(self):
        print(request.json)
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None or password is None:
            abort(400) # missing arguments
        if User.query.filter_by(username = username).first() is not None:
            abort(400) # existing user
        user = User(username = username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        # print(url_for('getuser', id = user.id, _external = True))
        return jsonify({'username': user.username})

class GetUser(Resource):
    def get(self, id):
        user = User.query.get(id)
        if not user:
            abort(400)
        return jsonify({'username': user.username})


class TirePrices(Resource):
    def get(self, region):
        parser = reqparse.RequestParser()
        # parser.add_argument('diametr', type=float, help='diameter of the tire')
        # parser.add_argument('width', type=int, help='width of the tire')
        # parser.add_argument('height', type=int, help='width of the tire')
        # parser.add_argument('count', type=int, help='count of records')
        # #Проверка на корректность ключей
        # args = parser.parse_args()
        # print(args)
        recCount=request.args['count']
        # print(args)
        args = request.args.to_dict() #flat=False
        del args['count']
        args_keys=list(args.keys())
        [abort_if_param_doesnt_exist(param) for param in args_keys]
        query=db.session.query(Tire.wear_num, Tire.unitPrice).filter_by(**args).limit(recCount)
        tires = query.all()
        # print(tires)
        tireList= []
        for tire in tires:
            tireList.append(tire._asdict())
        return jsonify(tireList)
