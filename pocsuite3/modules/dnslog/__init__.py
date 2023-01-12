from pocsuite3.modules.encryption import Encryption
import requests
import datetime
import json
import time
import re

# 功能 dnslog 模块用于无回显的漏洞
# 作者 charis
# 时间 2023-01-01
# 注意 服务端配置要和客户端一致

class Dnslog:

    # 初始化，设置token, api
    def __init__(self):

        self.headers = {
            "Cookie": "token=Kiss3389"
        }

        self.api = "http://ns1.charis3306.xyz:7001/revsuit/api/record/dns?page=1&pageSize=10&order=desc"


    def getDns(self, url, domain):
        # 10秒内找出与dns交互的数据
        r = requests.get(self.api, headers=self.headers)
        dictdata = json.loads(r.text)
        data = dictdata['result']['data']
        now = datetime.datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '%Y-%m-%d %H:%M:%S')
        for dnsVaule in data:
            d = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", dnsVaule['request_time']).group(0)
            t = re.search(r"(\d{1,2}:\d{1,2}:\d{1,2})", dnsVaule['request_time']).group(0)
            datas = d + " " + "" + t
            hello_time = (now - datetime.datetime.strptime(datas, '%Y-%m-%d %H:%M:%S')).seconds
            if hello_time <= 3:
                # return dnsVaule
                return self.getDnsMd5(url, data,domain)

    # md5 判断dns回显是否有发送的url
    def getDnsMd5(self, url, data, domain):

        for dnslog in data:
            try:
                flag = len(dnslog['flag'])
                domains = len(dnslog['domain']) - len(domain)  # 获取domain
                readd_commadn = dnslog['domain'][flag:domains - 1]  # 获取请求的地址和回显命令
                command = readd_commadn[readd_commadn.index(".") + 1:]  # 获取回显命令
                dnsurl = readd_commadn[:len(readd_commadn) - len(command) - 1]  # 获取请求地址信息
                if (Encryption().md5(url)) == str(dnsurl):
                    return f"dnslog 回显成功!请求地址为{url},回显命令执行结果{command}"
            except:
                pass

if __name__ == '__main__':
    print(Dnslog().getDns("http://www.baidu.com", "charis3389.xyz"))
