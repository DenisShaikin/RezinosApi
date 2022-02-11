from app import db
from flask import current_app as app
from flask import g
import pandas as pd
import time
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
import jwt


class Tire(db.Model):
    __tablename__ = 'tire'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(200))
    price = db.Column(db.Float)
    season = db.Column(db.String(20))
    region = db.Column(db.String(20))
    diametr = db.Column(db.Integer)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    wear= db.Column(db.String(10))
    qte= db.Column(db.Integer)
    unitPrice = db.Column(db.Float)
    wear_num = db.Column(db.Float)

    def __repr__(self):
        return '<Tire {} {}>'.format(self.id, self.brand)

    def load_tireprices(self):
        tirePrices = pd.read_csv(app.config['TIREPRICES_FILE'], encoding='utf-8', sep=';')
        tirePrices.index.name='id'
        tirePrices.to_sql('tire', con=db.engine, if_exists='replace', dtype={'id': db.Integer}, chunksize=10000)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def verify_password(username_or_token, password):
    #     # first try to authenticate by token
    #     user = User.verify_auth_token(username_or_token)
    #     if not user:
    #         # try to authenticate with username/password
    #         user = User.query.filter_by(username=username_or_token).first()
    #         if not user or not user.verify_password(password):
    #             return False
    #     g.user = user
    #     return True

    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')
        # s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        # return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        # s = Serializer(app.config['SECRET_KEY'])
        # try:
        #     data = s.loads(token)
        # except SignatureExpired:
        #     return None # valid token, but expired
        # except BadSignature:
        #     return None # invalid token
        # user = User.query.get(data['id'])
        # return user
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except:
            return
        return User.query.get(data['id'])
