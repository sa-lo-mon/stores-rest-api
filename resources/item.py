from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class ItemAPI(Resource):
    parser = reqparse.RequestParser()

    # extract from payload only the 'price' field
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field can't be empty"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.get(name)
        return {'item': item.json()}, 200 if item else 404

    def post(self, name):
        item = ItemModel.get(name)
        if item:
            return {"message": "An item with name '{}' already exists".format(name)}, 400  # 400 - Bad Request

        data = self.parser.parse_args()
        new_item = ItemModel(name, **data)

        try:
            new_item.save()
        except:
            return {'message':'An error occurred inserting the item'}

        return new_item.json(), 201

    def delete(self, name):
        item = ItemModel.get(name)
        if item:
            item.delete()
        return {'message': 'item was deleted'}

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.get(name)

        if item:
            item.price = data['price']
            message = 'item was updated'
        else:
            item = ItemModel(name, **data)
            message = 'item successfully inserted'

        item.save()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
        # return {"items": list(map(lambda x:x.json(), ItemModel.query.all()))}
