import redis
import re
from utils import configs
from utils.log_pag import logger

conn_redis = redis.Redis(host=configs.REDOSHOST, port=configs.REDOSPORT, db=configs.DB)


def sadd_proxy(proxy: str, process="Unprocessed"):
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
                # redis_set_key = re.sub(r"[^a-zA-Z0-9]", "", process)
                conn_redis.sadd(process, proxy)
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


def quantity(host: str):
    """Calculate the total number of domain agents"""
    return conn_redis.scard(host)


def random_proxy(amount: int, types="http", host=None):
    """Obtain random Number proxy"""
    types = types.lower()
    proxy_type_dict = {"http": configs.HTTP_PROCESSED, "https": configs.HTTPS_PROCESSED}
    types = proxy_type_dict.get(types)
    _count_key = (host or types)
    _count = quantity(_count_key)
    if amount > _count:
        amount = _count
    if host:
        proxy_list = conn_redis.srandmember(host, amount)
    else:
        proxy_list = conn_redis.srandmember(types, amount)
    return proxy_list

def add_host(host:str, url:str, amount:int, timeout:int, type:str):
    """
    1、入库host配置表
    :param host:
    :param url:
    :param amount:
    :param timeout:
    :param type:
    :return:
    """
    data = "{}|{}|{}|{}".format(url, type, amount, timeout)
    conn_redis.hset(configs.HOST_CONFIG, host, data)


def read_host():
    b_host_list = conn_redis.hkeys(configs.HOST_CONFIG)
    host_list = [host.decode("utf-8") for host in b_host_list]
    return {host: conn_redis.hget(configs.HOST_CONFIG, host) for host in host_list}





