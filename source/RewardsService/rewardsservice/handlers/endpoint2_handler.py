import json
import tornado.web
from pymongo import MongoClient
from tornado.gen import coroutine
from handlers.validators import EmailValidator


class Endpoint2Handler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        client = MongoClient('mongodb', 27017)
        db = client['Customers']
        email = self.get_argument('email', None)
        errors = []
        if not EmailValidator.valid_email(email):
            errors.append('missing or invalid email')
        customer = db.Customers.find_one({'Email Address': email}, {'_id': 0})
        if customer:
            # make list
            clist = []
            clist.append(customer)
            self.write(json.dumps(clist))
        else:
            errors.append('User not found')
        if errors:
            self.set_status(500)
            self.write(json.dumps({'errors': errors}))
            return None
