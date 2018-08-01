# # jwt原理
# import jwt
#
# key = "secret"
# token = jwt.encode({"payload": "abc123"}, key, "HS256").decode()
# print(token)
# print(jwt.decode(token, key, algorithms=["HS256"]))

# header, payload, signature = token.split(b".")
# print(header)
# print(payload)
# print(signature)
#
# import base64
#
# def addeq(b:bytes):
#     # 补齐等号
#     rem = len(b) % 4
#     return b + b"=" * rem
#
# print("header=", base64.urlsafe_b64decode(addeq(header)))
# print("payload=", base64.urlsafe_b64decode(addeq(payload)))
# print("signature=", base64.urlsafe_b64decode(addeq(signature)))
#
# from jwt import algorithms
#
# # 获取算法对象
# alg = algorithms.get_default_algorithms()["HS256"]
# newkey = alg.prepare_key(key)
#
# # 获取前两部分header、payload
# signing_input, _, _ = token.rpartition(b".")
# print(signing_input)
#
# # 使用key签名
# signature = alg.sign(signing_input, newkey)
# print(signature)


# import bcrypt
#
# password = b"123456"
#
# # 每次拿到的盐都不一样
# print(1, bcrypt.gensalt())
# print(2, bcrypt.gensalt())
#
# # 每次拿到的盐相同，计算得到的密文也相同
# salt = bcrypt.gensalt()
# x = bcrypt.hashpw(password, salt)
# print(3, x)
# x = bcrypt.hashpw(password, salt)
# print(4, x)
#
# # 每次拿到的盐不同，密文也不同
# x = bcrypt.hashpw(password, bcrypt.gensalt())
# print(5, x)
# x = bcrypt.hashpw(password, bcrypt.gensalt())
# print(6, x)
#
# # 校验密码
# print(bcrypt.checkpw(password, x), len(x))
# print(bcrypt.checkpw(password + b" ", x), len(x))


# jwt过期
import jwt
import threading
import datetime

event = threading.Event()
key = "wangjie"

date = jwt.encode({"name": "tom", "age": 20, "exp": int(datetime.datetime.now().timestamp()) + 5}, key)  # token中增加过期时间
print(jwt.get_unverified_header(date))
try:
    while not event.wait(1):
        print(jwt.decode(date, key))  # 检验过期，过期抛出异常
        print(datetime.datetime.now().timestamp())
except jwt.ExpiredSignatureError as e:
    print(e)

