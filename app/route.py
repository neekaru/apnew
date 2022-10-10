from app import app
from app.direct.basic import matching

@app.route("/")
def index():
    return "Testing"

@app.route("/direct", methods=["GET"])
def direct():
    if not request.args.get("url"):
        return
    query = request.args.get("url")
    try:
        return matching(query)
    except BaseException as b:
        return ({"Status": False, "msg": b})



