"""
@version: 3.6
@author: hewm
@file: clear_data.py
@time: 2019/10/10 15:33
@desc: 对数据进行清理的方法
"""
import re

def clear_str(sstr):
    """去除换行与回车"""
    return re.sub(r"\r|\n|", "", sstr).strip()

if __name__ == "__main__":
    k = "\r\n1231\r\n  "
    print(clear_str(k))