import requests
import base64
import json
import pyaes
import binascii
from datetime import datetime

a = 'http://api.skrapp.net/api/serverlist'
b = {
    'accept': '/',
    'accept-language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    'appversion': '1.3.1',
    'user-agent': 'SkrKK/1.3.1 (iPhone; iOS 13.5; Scale/2.00)',
    'content-type': 'application/x-www-form-urlencoded',
    'Cookie': 'PHPSESSID=fnffo1ivhvt0ouo6ebqn86a0d4'
}
c = {'data': '4265a9c353cd8624fd2bc7b5d75d2f18b1b5e66ccd37e2dfa628bcb8f73db2f14ba98bc6a1d8d0d1c7ff1ef0823b11264d0addaba2bd6a30bdefe06f4ba994ed'}
d = b'65151f8d966bf596'
e = b'88ca0f0ea1ecf975'

def f(g, d, e):
    h = pyaes.AESModeOfOperationCBC(d, iv=e)
    i = b''.join(h.decrypt(g[j:j+16]) for j in range(0, len(g), 16))
    return i[:-i[-1]]

j = requests.post(a, headers=b, data=c)

output_file_path = 'output.txt'

if j.status_code == 200:
    k = j.text.strip()
    l = binascii.unhexlify(k)
    m = f(l, d, e)
    n = json.loads(m)

    # 获取当前时间并格式化为字符串
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 创建一个时间节点
    time_node = f"aes-256-cfb:time_node@0.0.0.0:0"  # 使用占位符的节点信息
    time_node_base64 = base64.b64encode(time_node.encode('utf-8')).decode('utf-8')
    time_subscribe = f"ss://{time_node_base64}#{current_time}"
    
    with open(output_file_path, 'w') as file:  # 使用 'w' 模式覆盖写入文件
        # 写入时间节点到文件
        file.write(time_subscribe + '\n')
    
        for o in n['data']:
            p = f"aes-256-cfb:{o['password']}@{o['ip']}:{o['port']}"
            q = base64.b64encode(p.encode('utf-8')).decode('utf-8')
            r = f"ss://{q}#{o['title']}"
            print(r)
            file.write(r + '\n')  # 将输出写入文件
