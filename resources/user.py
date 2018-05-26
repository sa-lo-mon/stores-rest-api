from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot be empty'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot be empty'
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.get_by_username(data['username'])

        # check whether user already exist
        if user:
            return {"message": "A user with that username already exists"}, 400
        else:
            # iterates all dictionary keys in 'data' and insert their value to User object.
            # this way we create new User object easily
            user = UserModel(**data)
            user.save()
            return {"message": "User created successfully"}, 201
