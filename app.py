from flask import Flask, make_response
from flask_restx import Api, Resource, abort, reqparse
from logics import *

app = Flask(__name__)

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('tree', type=str, location='args', required=True)
parser.add_argument('limit', type=int, location='args', default=20)

@api.route('/paraphrase')
class TreeParaphraser(Resource):
    """Get paraphrased versions of bracketed tree string"""
    @api.expect(parser)
    def get(self):
        args = parser.parse_args()
        tree = nltk.ParentedTree.fromstring(args.get('tree'))
        limit = args.get("limit", 20)
        res = pull_list(tree)
        res.pop(0)
        if len(res) == 0:
            abort(400, "Can't paraphrase")
        output = []
        for i in res[:limit]:
            output.append({'tree': ' '.join(str(i).split())})
        return make_response({"paraphrases": output})





if __name__ == "__main__":
    app.run(port=5000, debug=True)
