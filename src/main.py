from flask import Flask
from flask_restful import Resource, Api
from setup_db import *
from model import *
import json


app = Flask(__name__)
api = Api(app)

class UserService(Resource):
    def get(self, username):
        user = {
            'username': "paulo_figueira",
            'name': "Paulo Figueira",
        }

        return { 'users': user }
    
class RecommendService(Resource):
    def get(self, username):
        bundles = [{
            "bundle_id": 1,
            "title": "This is a title",
            "description": "...",
            "instructions":  "...",
            "items": [
                {
                    "item_id": 2,
                    "quantity": 1,
                    "product": "acucar",
                    "image_url": "...",
                },
                {
                    "item_id": 3,
                    "quantity": 2,
                    "product": "farinha",
                    "image_url": "...",
                },
            ]
        }]
    
        return { 'bundles': bundles }

class BundleService(Resource):
    def get(self, username):
        bundle_recommendation = {
            "bundle_id": 1, 
            "title": "...",
            "start_date": "...",
            "end_date": "...",
            "description": "...",
            "instructions":  "...",
            "items": [
                {
                    "quantity": 1,
                    "product": "acucar",
                    "image_url": "...",
                },
                ...
            ]
        }
    
        return bundle_recommendation

api.add_resource(UserService, '/api/users/<string:username>')
api.add_resource(RecommendService, '/api/users/<string:username>/bundles')
api.add_resource(BundleService, '/api/users/<string:username>/bundles/<string:bundle_id>')

if __name__ == '__main__':
    conn = connect_db()
    setup_db(conn, cleanup=False)

    # model = compute_model("../datasets/sample_sales_info_encripted.csv", "../datasets/recipes.json")
    # bundle_ids = get_recommendations(model, 839934211079)

    #compute_model_db(conn, "../datasets/sample_sales_info_encripted.csv", "../datasets/recipes.json")
    bundle_ids = get_recommendations_db(conn, 839934211079)
    print(bundle_ids)

    app.run(host='0.0.0.0', port=5000, debug=True)