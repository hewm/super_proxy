import os
from flask import Flask
from flask import jsonify
from utils.redis_utils import smembers_proxy, random_proxy
app = Flask(__name__)
corrdic = {
    "HTTP": "HTTP_Unprocessed",
    "HTTPS": "HTTPS_Unprocessed"
}
app.secret_key = os.getenv('SECRET_KEY', "1231")
@app.route("/proxy_all", defaults={"typeof": "HTTP"}, methods=["GET"])
@app.route("/proxy_all/<any(HTTP, HTTPS):typeof>")
def proxy_all(typeof):
    """
    获取所有代理
    在类型大库中获取
    """
    if typeof in ["HTTP", "HTTPS"]:
        resp_dict = smembers_proxy(corrdic.get(typeof))
        resp_list = [str(i, encoding="utf-8") for i in resp_dict]
        return jsonify({"proxy": resp_list})
    else:
        return 500
@app.route("/proxy_random",defaults={"typeof": "HTTP", "host":None,"amount":5}, methods=["GET"])
@app.route("/proxy_random/<host>/<typeof>/<amount>")
def proxy_random(host, typeof, amount):
    resp_dict = random_proxy(amount, typeof, host)
    resp_list = [str(i, encoding="utf-8") for i in resp_dict]
    return jsonify({"proxy": resp_list})



if __name__ == "__main__":
    app.run()