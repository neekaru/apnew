from api_app import app, request, jsonify
from api_app.direct.basic import matching

@app.route("/")
def index():
    return "Testing"

@app.route("/direct", methods=["GET"])
def direk():
    if not request.args.get("url"):
        return
    query = request.args.get("url")
    try:
        return jsonify({"Status": True, "dl_link": matching(query)})
    except BaseException as b:
        return ({"Status": False, "msg": b})



