import requests
from lxml import etree
import time

class Kuaidaili():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.kuaidaili.com",
        "Pragma": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    start_url = "https://www.kuaidaili.com/free/inha/{}"

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
        for i in range(1, 50):
            url = self.start_url.format(i)
            response = self.get_url(url)
            time.sleep(5)
            if response:
                html = etree.HTML(response)
                proxy_list = html.xpath('//*[@id="list"]/table/tbody/tr')
                for proxy_type in proxy_list:
                    IP = proxy_type.xpath('string(./td[1]/text())')
                    PORT = proxy_type.xpath('string(./td[2]/text())')
                    INCOGNITO = proxy_type.xpath('string(./td[3]/text())')
                    TYPE = proxy_type.xpath('string(./td[4]/text())')
                    if INCOGNITO == "高匿名":
                        if TYPE == "HTTP":
                            pass
                        elif TYPE == "HTTPS":
                            pass
                        print(IP, PORT, TYPE)




if __name__ == "__main__":
    kdl = Kuaidaili()
    kdl.parse()