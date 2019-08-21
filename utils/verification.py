"""
url = www.baidu.com
验证模块
"""
import grequests
from utils.redis_utils import smembers_proxy
from utils.configs import HTTP_UNPROCESSED, HTTPS_UNPROCESSED, DEFAULT_HTTP, DEFAULT_HTTPS

# http_proxy = smembers_proxy(HTTP_UNPROCESSED)
# https_proxy = smembers_proxy(HTTPS_UNPROCESSED)


request_s = (grequests.get(url=DEFAULT_HTTP, proxies={"https": proxy}) for proxy in http_proxy)  # 异步url请求

exception_proxies = []
# 异常捕获方法
def exception_handler(request, exception):
    print(request.proxies)
    exception_proxies.append(request.proxies)
    print(exception)

response_list = grequests.map(request_s, size=1, exception_handler=exception_handler)

proxies_list = [response.proxies for response in response_list if response and response.status_code == 200]
for res_text in proxies_list:
    print(res_text)

if __name__ == "__main__":
    pass