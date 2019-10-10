from lxml import etree
import requests
from utils.redis_utils import sadd_proxy
from utils.clear_data import clear_str

class Iphai:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.iphai.com",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    start_url = "http://www.iphai.com/free/ng"

    def get_url(self, url):
        try:
            resp = requests.get(url=url, headers=self.headers)
            if resp.status_code == 200:
                return resp.text
            else:
                return ""
        except Exception as e:
            return ""

    def parse(self):
        response = self.get_url(self.start_url)
        if response:
            html = etree.HTML(response)
            # /html/body/div[2]/div[2]/table/tbody/tr[2]
            proxy_list = html.xpath('/html/body/div[2]/div[2]/table/tr')
            for proxy_type in proxy_list[1:]:
                IP = clear_str(proxy_type.xpath('string(./td[1]/text())'))
                PORT = clear_str(proxy_type.xpath('string(./td[2]/text())'))
                TYPE = clear_str(proxy_type.xpath('string(./td[4]/text())'))
                if TYPE == "":
                    proxy = "http://{}:{}".format(IP, PORT)
                    sadd_proxy(proxy, "Unprocessed")
                elif TYPE == "HTTPS":
                    proxy = "https://{}:{}".format(IP, PORT)
                    sadd_proxy(proxy, "Unprocessed")

if __name__ == "__main__":
    iphai = Iphai()
    iphai.parse()