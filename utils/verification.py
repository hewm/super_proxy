"""
url = www.baidu.com
验证模块
"""
import grequests
from utils.redis_utils import smembers_proxy,sadd_proxy,del_proxy
from utils.proxy_main import Main_proxy
from utils.configs import HTTP_UNPROCESSED, HTTPS_UNPROCESSED, DEFAULT_URL, SIZE
from utils.log_pag import logger

http_proxy = smembers_proxy(HTTP_UNPROCESSED)
https_proxy = smembers_proxy(HTTPS_UNPROCESSED)

proxy_dict = {
    "http": http_proxy,
    "https": https_proxy
}

request_s = (grequests.get(url=DEFAULT_URL[key], proxies={key: proxy}, timeout=30) for key, val in proxy_dict.items() for proxy in val)  # 异步url请求

delete_proxy_https = Main_proxy.save_proxy
delete_proxy_http = Main_proxy.save_proxy
insert_proxy_https = Main_proxy.save_proxy
insert_proxy_http = Main_proxy.save_proxy


def exception_handler(request, exception):
    if request.kwargs.get("proxies").get("https"):
        delete_proxy_https.append(request.kwargs.get("proxies").get("https"))
        logger().logger.error("[报错代理]   {}".format(request.kwargs.get("proxies").get("https")))
    if request.kwargs.get("proxies").get("http"):
        delete_proxy_http.append(request.kwargs.get("proxies").get("http"))
        logger().logger.error("[报错代理]   {}".format(request.kwargs.get("proxies").get("http")))


response_list = grequests.map(request_s, size=SIZE, exception_handler=exception_handler)
proxies_list = [response for response in response_list if response and response.status_code == 200]

for res_text in proxies_list:
    if res_text.raw._pool.proxy.scheme == "http":
        insert_proxy_http.append("http://" + res_text.raw._pool.proxy.host+":"+str(res_text.raw._pool.proxy.port))
    else:
        insert_proxy_https.append("https://" + res_text.raw._pool.proxy.host+":"+str(res_text.raw._pool.proxy.port))

[sadd_proxy(i, "Processed") for i in insert_proxy_https]
[sadd_proxy(i, "Processed") for i in insert_proxy_http]
[sadd_proxy(i, "Scrapped") for i in delete_proxy_https]
[sadd_proxy(i, "Scrapped") for i in delete_proxy_http]
[del_proxy(i)for i in http_proxy]
[del_proxy(i)for i in https_proxy]

if __name__ == "__main__":
    pass