from flask import Flask, jsonify
from flask_restx import Api, Resource, abort, reqparse
from logics import *

example = """
(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP
Quarter) ) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic) ) ) (, ,) (VP (VBZ has) (NP (NP
(JJ narrow) (JJ medieval) (NNS streets) ) (VP (VBN filled) (PP (IN with) (NP (NP (JJ
trendy) (NNS bars) ) (, ,) (NP (NNS clubs) ) (CC and) (NP (JJ Catalan) (NNS
restaurants) ) ) ) ) ) ) )"""

app = Flask(__name__)

api = Api(
    title="Tree paraphraser",
    version="1.0",
    description="Paraphrases syntax trees",
)

api.init_app(app)
parser = reqparse.RequestParser()
parser.add_argument("tree", type=str, location="args", required=True, default=example)
parser.add_argument("limit", type=int, location="args", default=20)

@api.route("/paraphrase")
class TreeParaphraser(Resource):
    """Get paraphrased versions of bracketed tree string"""

    @api.expect(parser)
    @api.doc(responses={200: "Success", 400: "Validation Error"})
    def get(self):
        args = parser.parse_args()
        tree = nltk.ParentedTree.fromstring(args.get("tree"))
        limit = args.get("limit", 20)
        res = pull_list(tree)
        res.pop(0)
        if len(res) == 0:
            abort(400, "Can't paraphrase")
        output = []
        for i in res[:limit]:
            output.append({"tree": " ".join(str(i).split())})
        return jsonify({"paraphrases": output})


if __name__ == "__main__":
    app.run(debug=True)
