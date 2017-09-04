import json
import tornado.web
from pymongo import MongoClient
from tornado.gen import coroutine


class Endpoint3Handler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        client = MongoClient('mongodb', 27017)
        db = client['Customers']
        errors = []
        customers = list(db.Customers.find({}, {'_id': 0}))
        print(customers)
        if customers:
            self.write(json.dumps(customers))
        else:
            errors.append('User not found')
        if errors:
            self.set_status(500)
            self.write(json.dumps({'errors': errors}))
            return None
