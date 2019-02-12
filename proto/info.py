import rsa
from proto.util import *
from config.config import *


class ChatInfo(object):
    """聊天信息"""

    # 密钥信息
    aes_key = ""
    rsa_public_key_name = ""
    rsa_private_key_name = ""

    # 主聊天者(发起加密聊天的好友)
    chat_master = False

    # 期望确认消息个数
    expect_ack_count = 0

    # 实际已确认消息个数
    actual_ack_count = 0

    # 密钥数组
    key_info_list = list()

    # 协商成功标志
    is_chat_ready = False

    # 聊天id协商成功标志
    is_id_ready = False

    # 时间戳
    time = ""

    # 好友ID
    user_id = ""

    # 好友名称
    user_name = ""

    def __init__(self):
        """"初始化"""
        self.is_chat_ready = False
        self.is_id_ready = False
        self.expect_ack_count = 0
        self.actual_ack_count = 0
        self.chat_user_name = ""
        self.rsa_public_key_name = ""
        self.rsa_private_key_name = ""
        self.chat_master = False
        self.time = ""
        self.user_name = ""

    def set_aes_key(self, key):
        self.aes_key = key

    def get_aes_key(self):
        return self.aes_key

    def set_rsa_key(self, public_key, private_key):
        self.rsa_public_key_name = public_key
        self.rsa_private_key_name = private_key

    def get_rsa_key(self):
        return self.rsa_public_key_name, self.rsa_private_key_name

    def get_rsa_public_key(self):
        return self.rsa_public_key_name

    def get_rsa_private_key(self):
        return self.rsa_private_key_name

    def gen_new_rsa_key(self):
        # todo
        return


class FriendInfo:
    """
    微信好友信息
    """
    user_id = ""
    nick_name = ""
    remark_name = ""
    friend_count = 0

    def __init__(self, user_id='', nick_name='', remark_name='', friend_count=0):
        self.user_id = user_id
        self.nick_name = nick_name
        self.remark_name = remark_name
        self.friend_count = friend_count


class KeyInfo:
    """
        密钥信息
    """
    user_id = ""
    aes_key = ""
    time_stamp = ""

    def __init__(self, user_id='', aes_key='', time_stamp=''):
        self.user_id = user_id
        self.aes_key = aes_key
        self.time_stamp = time_stamp

# # 测试代码
# chat = ChatInfo()
# print(type(chat.aes_key))
# chatObj = list()
# chatObj.append(ChatInfo())
# chatObj.append(ChatInfo())
#
# for i in chatObj:
#     print(i.aes_key)
#     print(i.rsa_private_key_name)