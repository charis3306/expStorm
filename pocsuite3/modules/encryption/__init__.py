# 功能 加解密 模块用于加解密使用
# 作者 charis
# 时间 2023-1-1

import hashlib
class Encryption():
    # 定义md5加密
    def md5(self, string):
        md5 = hashlib.md5()
        md5.update(string.encode(encoding='utf-8'))
        return md5.hexdigest()

if __name__ == '__main__':
    md5 = Encryption().md5("test")
    print(md5)