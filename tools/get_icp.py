import requests
from socket import getaddrinfo
from lxml import etree
requests.packages.urllib3.disable_warnings()

# 功能 dnslog 备案查询
# 作者 周佳豪
# 时间 2023-01-19

class getICP:
    def __init__(self, domin):
        self.domin = domin
        self.header = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Connection": "close"
        }
        self.result = ""
        if self.check():
            self.check(self.ipToDomin(self.domin))

        self.result = self.getDomin()

    def check(self, domin="") -> bool:
        self.domin = self.domin if domin == "" else domin

        lenNum = len(self.domin) // 2

        if "http" in self.domin[:lenNum] or "www" in self.domin[:lenNum]:
            self.domin = self.domin.replace("https://",'').replace('www.','').replace('https:\\\\','').replace('/','')
            return False

        if self.domin[-1].isdigit():
            return True
        return False

    def getDomin(self, domin="") -> tuple:
        self.domin = self.domin if domin == "" else domin

        try:
            req = requests.get(url=f"https://api.vvhan.com/api/icp?url={self.domin}", headers=self.header, timeout=20)
            if req.status_code != 200:
                return ("超时",False)

            if len(req.json()) != 2 :
                return (req.json()["info"]["name"], req.json()["info"]["nature"], req.json()["info"]["title"],req.json()["info"]["icp"],True)

            elif req.json()["message"] == "请输入正确的域名":
                return ("域名格式错误", False)
            else:#此域名未备案
                try:
                    try:
                        return (self.ipToDomin(getaddrinfo(self.domin, 'http')[0][4][0]), False)
                    except:
                        print(111111)
                        print(self.domin)
                        return (getaddrinfo(self.domin, 'http')[0][4][0], False)
                except:
                    return ("此域名未备案 且 ip获取失败",False)

        except Exception as e:
            return ("程序异常",False)


    def ipToDomin(self, ip):
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            #     "Connection": "close"  数据量传输慢 不可立马关闭socket通道
        }

        try:
            req1 = requests.get(url=f"https://ipchaxun.com/{ip}", headers=headers, timeout=20, verify=False)
            if req1.status_code != 200:
                return "错误200"

            if req1.text != "null":
                html = etree.HTML(req1.text)
                try:
                    domin = html.xpath('//div[@id="J_domain"]/p/a/text()')[0]
                    if domin == "":
                        raise ValueError("domin获取失败1")

                    return domin
                except:
                    return "domin获取失败2"

        except Exception as e:
            pass

        return "domin获取失败3"

    def __str__(self):
        return str(self.result)


if __name__ == '__main__':
    print(getICP(getICP("180.101.50.172")))

