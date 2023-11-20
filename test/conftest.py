# import os
# import pytest
# import dotenv
#
# from fastapi.testclient import TestClient
#
# from main import app
# from app.crud.token import delToken
# from app.utils.log import logger
# from app.db.redis import get_redis
#
#
# dotenv.load_dotenv()
#
#
# API_KEY = os.getenv("FIRE_BASE_API_KEY")
#
# # #https://github.com/jewang/firebase-id-token-generator-python/blob/master/firebase_token_generator.py
# # def get_token(uid):
# #
# #   token = create_custom_token(uid)
# #   data = {
# #     'token': token,
# #     'returnSecureToken': True
# #   }
# #
# #   url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty" \
# #         "/verifyCustomToken?key={}".format(API_KEY)
# #
# #   req = Request(url,json.dumps(data),{'Content-Type': 'application/json'})
# #   response = urlopen(req).read()
# #
# #   return json.loads(response)
#
# testUID = os.getenv("TEST_USER_UID")
# testToken = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImM2NzNkM2M5NDdhZWIxOGI2NGU1OGUzZWRlMzI1NWZiZjU3NTI4NWIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZGVsaXZlcnMtdHJhdmVscyIsImF1ZCI6ImRlbGl2ZXJzLXRyYXZlbHMiLCJhdXRoX3RpbWUiOjE2NTEyMTEyMzUsInVzZXJfaWQiOiJnTWFxVGp5eFpCUXM1T3Q1cFpHM215UXZLZXExIiwic3ViIjoiZ01hcVRqeXhaQlFzNU90NXBaRzNteVF2S2VxMSIsImlhdCI6MTY1MTIxMTIzNiwiZXhwIjoxNjUxMjE0ODM2LCJlbWFpbCI6Impja2ltMDMwN0BoYW55YW5nLmFjLmtyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiamNraW0wMzA3QGhhbnlhbmcuYWMua3IiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.WJS9Y3DSvAGgYOV4P2LyIEYOZSBBHwkPZlhedIzZvcGHfMXKmJuFZiKzhOLT26Svoi1wbyVKTtJqNCjgW99GkdNR77w6rqZphVo-DmcY9947Crb4A0GgW9yXrkxgoRxNRvENIWDwddsSPxEBc3vvIIUWv7HfhyTXlQzf0eQWRISu9lJRHlL5bFcztTJrne-8slGgrmY2eE-2EwBdgCnuMQaX084KXm9-ZIBQkbNEyBgrz0cYhmZKiEOXSlYR9fCpZhaGlPBoKuMpr59KvHq-Zg_hiBNH6hXWb_ywTPpj2vWOPXsBRw6xTFr1onGXPJ17KjrZM01gT7PuWsxmV_y3TA"
# testFakeToken = "SIGONG" * 21 + "gg"
#
#
# @pytest.fixture
# def fastapi_client():
#     fastapi_client = TestClient(app)
#     return fastapi_client
#
#
# @pytest.fixture
# def idx_redis():
#     idx_redis = get_redis()
#     return idx_redis
#
#
# @pytest.fixture(autouse=True)
# def setup():
#     redis = get_redis()
#     delToken(testToken, redis)
#     logger.debug(f"test before set up // create testToken {testToken}")
#
#
# @pytest.fixture(autouse=True)
# def teardown():
#     yield
#     redis = get_redis()
#     delToken(testToken, redis)
#     logger.debug(f"test is fin, teardown")
