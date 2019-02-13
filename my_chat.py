# -*- coding: utf-8 -*-
import itchat
import sys
import os
import importlib
import threading
from constants.type import *
from itchat.content import *
from proto.info import *
from proto.proto import IdAgreement
from proto.proto import KeyAgreement
from proto.util import UtilTool

sys.path.append(os.getcwd() + '/constants')

importlib.reload(sys)

my_id = ''
mutex = threading.Lock()

# 信息类对象
my_info = MyInfo()

global_cur_chatter_name = "AA"
# global_cur_chatter_name = "贝贝奶奶"

global_cur_chatter_id = ""


def say():
    global global_cur_chatter_id
    while True:
        my_msg = input()
        print('我: ', end='')

        # 选择/切换聊天对象
        if my_msg.startswith(CHAT_START):
            user_name = my_msg.lstrip(CHAT_START)
            global_cur_chatter_id = KeyAgreement.launch_key_agreement(user_name, my_info)
            continue

        # 协商完成,加密通信
        if IdAgreement.is_key_agreement_ready(my_info, global_cur_chatter_id):
            chat_id = my_info.get_user_id_to_chat_id(global_cur_chatter_id)
            # 加密信息
            chat_info = my_info.get_chat_id_to_chat_info(chat_id)
            ase_key = chat_info.aes_key
            en_msg = UtilTool.aes_encrypt(ase_key, my_msg)
            itchat.send_msg(en_msg, toUserName=global_cur_chatter_id)
        else:
            print("密钥协商未完成，请等待协商完成")


# 微信消息类型 TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, VIDEO
@itchat.msg_register([TEXT, ATTACHMENT], isFriendChat=True, isGroupChat=True, isMpChat=True)
def listen(receive_msg):
    print('Receive New Msg:', receive_msg)
    global my_id

    if not hasattr(receive_msg, 'Text') and not hasattr(receive_msg, 'Type'):
        return

    # 接收到chat_id
    if receive_msg.Type == WX_TEXT and receive_msg.Text.startswith(CHAT_ID_START):
        IdAgreement.id_ack(receive_msg, my_info)
        return

    # 接受到chat_id确认消息
    if receive_msg.Type == WX_TEXT and receive_msg.Text.startswith(CHAT_ID_ACK):
        chat_id = receive_msg.Text.lstrip(CHAT_ID_ACK)
        if my_info.check_chat_id_to_chat_info(chat_id):
            chat_info = my_info.get_chat_id_to_chat_info(chat_id)
            chat_info.expect_ack_count += 1
        else:
            print('聊天ID协商异常，程序退出')
        return

    # 收到rsa公钥文件，密钥协商步骤二
    if receive_msg.Type == WX_ATTACHMENT:
        KeyAgreement.key_agreement_step_two(receive_msg, my_id, my_info)
        return

    #  收到aes密钥，返回密钥协商步骤三
    if receive_msg.Type == WX_TEXT and receive_msg.Text.startswith(AES_KEY):
        print('密钥协商步骤三')
        if my_info.check_user_id_to_chat_id(receive_msg.FromUserName):
            KeyAgreement.key_agreement_step_three(receive_msg, my_info)
        else:
            print('密钥协商异常, 程序退出')
        return

    # 保存aes密钥, 密钥协商步骤四
    if receive_msg.Type == WX_TEXT and receive_msg.Text.startswith(my_id) and my_info.check_user_id_to_chat_id(
            receive_msg.FromUserName):
        print('密钥协商步骤四')
        print("my_id",my_id)
        KeyAgreement.key_agreement_step_four(receive_msg, my_id, my_info)
        print('密钥协商完成，开始加密聊天')
        return

    # 开始加密聊天
    UtilTool.encrypt_chat(receive_msg, global_cur_chatter_id, my_info)


def init_mychat():
    global global_cur_chatter_id
    global my_id
    # 初始化朋友列表
    my_id = UtilTool.init_friends(my_info)

    # 初始化好友群信息
    UtilTool.init_rooms(my_info)

    # 初始化当前聊天好友
    global_cur_chatter_id = UtilTool.init_current_friend(global_cur_chatter_name, my_info)

    # 删除无用的密钥文件
    UtilTool.remove_unused_file()

    print('init success')


if __name__ == '__main__':
    itchat.auto_login()  # hotReload=True
    init_mychat()
    # 启动线程
    t1 = threading.Thread(target=say)
    t2 = threading.Thread(target=listen, args=(u'',))
    t1.start()
    t2.start()

    itchat.run()
