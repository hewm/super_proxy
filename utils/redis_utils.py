import redis
import re
from utils import configs
from utils.log_pag import logger

conn_redis = redis.Redis(host=configs.REDOSHOST, port=configs.REDOSPORT, db=configs.DB)


def sadd_proxy(proxy, process="Unprocessed"):
    """redis insert set"""
    try:
        if process == "Unprocessed":
            if "https" in proxy:
                conn_redis.sadd(configs.HTTPS_UNPROCESSED, proxy)
            elif "http" in proxy:
                conn_redis.sadd(configs.HTTP_UNPROCESSED, proxy)
        elif process == "Processed":
            if "https" in proxy:
                conn_redis.sadd(configs.HTTPS_PROCESSED, proxy)
            elif "http" in proxy:
                conn_redis.sadd(configs.HTTP_PROCESSED, proxy)
        elif process == "Scrapped":
            if "https" in proxy:
                conn_redis.sadd(configs.HTTPS_SCRAPPED, proxy)
            elif "http" in proxy:
                conn_redis.sadd(configs.HTTP_SCRAPPED, proxy)
        else:
            if process:
                redis_set_key = re.sub(r"[^a-zA-Z0-9]", "", process)
                conn_redis.sadd(redis_set_key, proxy)
    except Exception as e:
        logger().logger.error("[sadd error]   \n{}".format(e))


def smembers_proxy(htype: str):
    """Obtain all proxy"""
    try:
        proxy_lsit = conn_redis.smembers(htype)
        return proxy_lsit
    except Exception as e:
        logger().logger.error("[smembers_proxy error]   \n{}".format(e))


def del_proxy(proxy: str, process="Unprocessed"):
    try:
        if process == "Unprocessed":
            if "https" in proxy:
                conn_redis.srem(configs.HTTPS_UNPROCESSED, proxy)
            elif "http" in proxy:
                conn_redis.srem(configs.HTTP_UNPROCESSED, proxy)
        elif process == "Processed":
            if "https" in proxy:
                conn_redis.srem(configs.HTTPS_PROCESSED, proxy)
            elif "http" in proxy:
                conn_redis.srem(configs.HTTP_PROCESSED, proxy)
        else:
            if "https" in proxy:
                conn_redis.srem(configs.HTTPS_SCRAPPED, proxy)
            elif "http" in proxy:
                conn_redis.srem(configs.HTTP_SCRAPPED, proxy)
    except Exception as e:
        logger().logger.error("[del_proxy error]   \n{}".format(e))



