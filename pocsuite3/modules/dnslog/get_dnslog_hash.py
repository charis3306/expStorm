from pocsuite3.modules.encryption import Encryption
import requests
import json
import os

# 功能 dnslog 模块用于无回显的漏洞
# 作者 charis
# 时间 2023-01-02
# 要说的话，对于无回显的，使用hash校验的方式，确定漏洞的准确性，相比时间差+hash校验的方式效率更高
# 首先使用后时间差+hash校验，校验完成后，用此模块来定位资产


class GetDnslogHash():

    def __init__(self):
        # 定义token
        self.headers = {
            "Cookie": "token=Kiss3389"
        }

    # 根据页数返回需要的值
    def getHashpage(self, page):
        api = f"http://ns1.charis3306.xyz:7001/revsuit/api/record/dns?page={page}&pageSize=10&order=desc"
        r = requests.get(api, headers=self.headers)
        dictdata = json.loads(r.text)
        return dictdata


    #返回全部数据的数量
    def getDnslogcount(self):
        api = f"http://ns1.charis3306.xyz:7001/revsuit/api/record/dns?page=1&pageSize=1&order=desc"
        r = requests.get(api, headers=self.headers)
        dictdata = json.loads(r.text)
        count = dictdata['result']['count']
        return count

    # 返回全部数据的请求地址
    def getHash(self, domain):

        dnslist = []  # 保存返回dns请求地址
        for getvalue in range(1, (self.getDnslogcount()//10) +2):
            data = self.getHashpage(getvalue)['result']['data']
            for dnslog in data:
                try:
                    flag = len(dnslog['flag'])
                    domains = len(dnslog['domain']) - len(domain)  # 获取domain
                    readd_commadn = dnslog['domain'][flag:domains - 1]  # 获取请求的地址和回显命令
                    command = readd_commadn[readd_commadn.index(".") + 1:]  # 获取回显命令
                    dnsurl = readd_commadn[:len(readd_commadn) - len(command) - 1]  # 获取请求地址信息
                    dnslist.append(dnsurl)
                except:
                    pass
        return dnslist

    # 全部hash保存到文件中，加快比较速度
    def outHash(self):
        hashdata = ""
        for hash in self.getHash("charis3389.xyz"):
            hashdata += hash + "\n"
        with open(r"../../data/hashdata.txt", "w",
                  encoding="utf-8") as f:
            f.write(hashdata)

    # 读取本地文件获和在的记录同步，获取漏掉的漏洞
    def createHash(self, path, domain):
        listresult = []
        n = 0
        path = repr(path).replace("\\\\", "\\").replace("'", "")  # 参入的参数进行原格式防止被转义
        path = os.path.expanduser(path)  # 支持linux windows 平台路径
        # 打开从远程获取的hash
        self.outHash()
        with open(r"../../data/hashdata.txt", "r", encoding="utf-8") as f:
            hashlistdata = f.readlines()

        with open(path, "r",encoding="utf-8") as f:
            for value in f.readlines():
                for rednsdata in hashlistdata:
                    if rednsdata.strip("\n") == Encryption().md5(value.strip("\n")):
                        n += 1
                        readd = value.strip("\n") #请求地址
                        rehash = Encryption().md5(value.strip("\n")) #请求hash
                        listresult.insert(n, f"利用成功：请求地址：{readd} md5值为：{rehash}")

        return set(listresult)

if __name__ == '__main__':
    # 实例

    path = r'C:\Users\charis\Documents\GitHub\expStorm\target\host.txt'
    result = GetDnslogHash().createHash(path, "charis3389.xyz")
    for i in result:
        print(i)
