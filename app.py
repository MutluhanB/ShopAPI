from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required


app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    #HTTP Request parser
    parser = reqparse.RequestParser()
    parser.add_argument("price",
    type = float,
    required = True,
    help="Please provide price information"
    )
    #GET /item/<name>
    def get(self, name):
        #Filter the item list with given name, return None if it is not found.
        item = next(filter(lambda x: x["name"] == name, items), None)

        #Return the item with code 200 if item exist. Else return 404
        return {"Item": item}, 200 if item else 404

    #POST /item/<name>
    def post(self, name):
        #Filtering the list to raise error if item already exist.
        #if filter not returns None execute the if block. Same thing as filter.... is not none.
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"message": "An item with name '{}' already exist.".format(name)},400

        data = Item.parser.parse_args()
        item = {"name":name, "price": data["price"]}
        items.append(item)
        return item, 201

    #DELETE /item/<name>
    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name,items))
        return {"message": "item deleted"}

    #PUT /item/<name>
    #Updates price of an item
    def put(self,name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x["name"] == name,items),None)
        if item is None:
            item = {"name":name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item
class ItemList(Resource):
    #GET /items
    def get(self):
        return {"items": items}

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
app.run(port=5000, debug=True)
