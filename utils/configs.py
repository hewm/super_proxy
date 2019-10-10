REDOSHOST = "127.0.0.1"
REDOSPORT = 6379
DB = 0

# set list
HTTP_UNPROCESSED = "HTTP_Unprocessed"  # 未经处理的HTTP代理
HTTPS_UNPROCESSED = "HTTPS_Unprocessed"  # 未经处理的HTTPS代理
HTTP_PROCESSED = "HTTP_Processed"  # 经过httpbin验证HTTP代理
HTTPS_PROCESSED = "HTTPS_Processed"  # 经过httpbin验证HTTPS代理
HTTP_SCRAPPED = "HTTP_Scrapped"  # 不可用HTTP[报废库] [每条超时时间30天]
HTTPS_SCRAPPED = "HTTPS_Scrapped"  # 不可用HTTPS[报废库] [每条超时时间30天]
HOST_CONFIG = "HOST_config"  # host 配置表

# log pag
LOG_PATH = "../log/logs.log"

# default url
DEFAULT_URL = {
    "http": "http://httpbin.org/get",
    "https": "https://httpbin.org/get"
}

# 验证并发数配置

SIZE = 50