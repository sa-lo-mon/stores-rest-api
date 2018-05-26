from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        else:
            return {'message': "Store wasn't found"}, 404


    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "An item with name '{}' already exists".format(name)}, 400  # 400 - Bad Request

        store = StoreModel(name)

        try:
            store.save()
        except:
            return {'message': 'An error occurred inserting the store'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()
        return {'message': 'store was deleted'}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
        # return {"items": list(map(lambda x:x.json(), ItemModel.query.all()))}
