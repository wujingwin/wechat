# -*- coding:utf-8 -*-
import time
import xmltodict
from flask import Flask, request
import hashlib

WECHAT_TOKEN = 'itheima'

app = Flask(__name__)

@app.route('/wechatsz8008',methods=['GET','POST'])
def index():
    # signature：微信加密签名
    signature = request.args.get('signature')
    # timestamp：时间戳
    timestamp = request.args.get('timestamp')
    # nonce：随机数
    nonce = request.args.get('nonce')
    # echostr：随机字符串
    echostr = request.args.get('echostr')

    # 校验微信发送的参数，确定次这个GET请求是微信发送的
    # 1）将token、timestamp、nonce三个参数进行字典序排序
    tmp_list = [WECHAT_TOKEN, timestamp, nonce]
    tmp_list.sort()

    # 2）将三个参数字符串拼接成一个字符串进行sha1加密
    tmp_str = ''.join(tmp_list)
    sin_str = hashlib.sha1(tmp_str).hexdigest()

    # 3）开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
    if sin_str == signature:

        if request.method=='POST':
            xml_str = request.data
            xml_dict= xmltodict.parse(xml_str)
            request_dict = xml_dict.get('xml')
            # 获取类型
            #获取类型
            msg_type = request_dict.get('MsgType')

            if msg_type=='text':
                 # 说明用户发送的文本消息
                 new_dict = {
                     'ToUserName': request_dict.get('FromUserName'),
                     'FromUserName': request_dict.get('ToUserName'),
                     'CreateTime': time.time(),
                     'MsgType': 'text',
                     'Content': u'你有8848吗？'
                 }

                 print request_dict.get('Content')
                 # 封装响应的字典
                 response_dict = {'xml': new_dict}

                 # 将响应的字典转成xml字符串
                 response_xml_str = xmltodict.unparse(response_dict)
                 # 发送xml字符串给微信服务器，然后服务器转到到粉丝
                 return response_xml_str

            elif msg_type=='voice':
                # 说明用户发送的文本消息
                new_dict = {
                    'ToUserName': request_dict.get('FromUserName'),
                    'FromUserName': request_dict.get('ToUserName'),
                    'CreateTime': time.time(),
                    'MsgType': 'text',
                    'Content': u'谢谢诶'
                }

                print request_dict.get('Content')
                # 封装响应的字典
                response_dict = {'xml': new_dict}

                # 将响应的字典转成xml字符串
                response_xml_str = xmltodict.unparse(response_dict)
                # 发送xml字符串给微信服务器，然后服务器转到到粉丝
                return response_xml_str
            else:
                return echostr  # 告诉微信服务器。我给你的IP是OK的

    return ''  # 告诉微信服务不可用

if __name__ == '__main__':
    app.run(debug=True,port=8008)