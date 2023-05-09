# expStorm
 基于pocsuite3编写的expStorm漏洞检测工具
 感谢 pocsuite3 

 https://github.com/knownsec/pocsuite3.git
# 该项目不在维护，会重新构建新的项目。
## 目前版本
支持 windows linux 平台

使用方法

```
pip3 install -r requirements.txt
python3 expStorm.py -h
```

注意：请配置tools目录和pocsuite3\modules\dnslog\__ini__.py目录下revsuit的token 和api接口 用于无回显漏洞检测。

```commandline

def __init__(self):
    # 定义token
    self.headers = {
        "Cookie": "token="
    }
```

例如：探测xxl-job未授权rec漏洞
使用10个线程对指定xxl-job.txt文件内的资产进行测试并输入html格式
```commandline
python .\expStorm.py -r .\pocs\web\XXL-JOB\xxl-job-unauth-access.py -f .\target\xxl-job.txt --domain "charis3389.xyz" --threads 10 --plugins .\pocsuite3\plugins\html_report.py
```



## 更新日志0.1.1
1. 针对无回显poc验证编写了一个接口，此接口可以使用自建dnslog
2. 目前支持自建dnslog平台 revsuit


## revsuit

项目链接如下：https://github.com/Li4n0/revsuit.git

## 技术细节

针对无回显漏洞，验证通过率为100%！
1. 针对无回显漏洞验证，使用时间差加hash校验双重校验
2. 存在漏洞的url转成md5记录到dnslog服务器中，时间差和hash校验完成后，dnslog记录会下发到客户端，随后客户端和服务端再次hash校验方式，再次验证漏洞是否存在误报。



## 联系我

CHARIS3306@OUTLOOK.COM 

