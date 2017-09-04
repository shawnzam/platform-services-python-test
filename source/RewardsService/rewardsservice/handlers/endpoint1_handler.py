import json
# import re
import math
import tornado.web
from pymongo import MongoClient
from tornado.gen import coroutine
from handlers.validators import EmailValidator


class Endpoint1Handler(tornado.web.RequestHandler):

    def find_tier(self, points, rewards, increment):
        rewards.insert(0, {
            'rewardName': '0% off purchase',
            'tier': 'Z',
            'points': 0
        })
        return next((reward for reward in rewards if reward['points'] > points - increment), rewards[-1])

    def calc_progress(self, tier_points, next_tier_points, customer_current_points):
        if (next_tier_points - tier_points) > 0:
            return (customer_current_points - tier_points) / (next_tier_points - tier_points)
        else:
            return 0

    @coroutine
    def post(self):
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        client = MongoClient('mongodb', 27017)
        db = client['Rewards']
        rewards = list(db.rewards.find({}, {'_id': 0}))
        db = client['Customers']
        email = self.get_body_argument('email', None)
        cost = self.get_body_argument('cost', None)
        errors = []
        if not EmailValidator.valid_email(email):
            errors.append('missing or invalid email')
        try:
            cost = float(cost)
        except ValueError:
            errors.append('missing or invalid cost')
        if errors:
            self.set_status(500)
            self.write(json.dumps({'errors': errors}))
            return None
        customer = db.Customers.find_one({'email': email}, {'_id': 0})
        customer_current_points = 0
        if not customer:
            customer_current_points = math.floor(cost)
            db.Customers.insert(
                {'email': email, 'customer_current_points': math.floor(cost)})
        else:
            customer_current_points = customer[
                'customer_current_points'] + math.floor(cost)
        tier = self.find_tier(customer_current_points, rewards, 100)
        next_tier = self.find_tier(customer_current_points, rewards, 0)
        x = db.Customers.update({'email': email}, {
            'email': email,
            'customer_current_points': customer_current_points,
            'Rewards Tier': tier['tier'],
            'Reward Tier Name': tier['rewardName'],
            'Reward Points': tier['points'],
            'Next Rewards Tier': next_tier['tier'],
            'Next Rewards Tier Name': next_tier['rewardName'],
            'Next Rewards Tier Progress': self.calc_progress(tier['points'], next_tier['points'], customer_current_points)})
        customer = db.Customers.find_one({'email': email}, {'_id': 0})
        self.write(customer)
