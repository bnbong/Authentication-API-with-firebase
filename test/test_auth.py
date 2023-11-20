# import pytest
#
# from conftest import testToken, testFakeToken, testUID
#
# from app.crud.token import createToken, findByToken
# from app.db.redis import get_redis
#
#
# # 인증이 실패하는지 여부
# @pytest.mark.asyncio
# async def test_get_False(fastapi_client, idx_redis):
#     response = fastapi_client.get(f"/api/v1/auth/verify/{testFakeToken}")
#
#     assert response.status_code == 200
#     assert response.json() == {"verify": False}
#     assert await findByToken(testFakeToken, idx_redis) is False
#
#
# # 캐시에 데이터가 없을 때, 인증이 정상적으로 이루어지는지 여부
# def test_non_lookaside_get_True(fastapi_client):
#     response = fastapi_client.get(f"/api/v1/auth/verify/{testToken}")
#     assert response.status_code == 200
#     assert response.json() == {"verify": True}
#
#
# # 캐시에 데이터가 있을 때, 인증이 정상적으로 이루어지는지 여부
# @pytest.mark.asyncio
# async def test_get_lookaside_non_info_get_True(fastapi_client, idx_redis):
#     await createToken(testToken, 180, testUID, idx_redis)
#     response = fastapi_client.get(f"/api/v1/auth/verify/{testToken}")
#
#     assert response.status_code == 200
#     assert response.json() == {"verify": True}
#
#
# # 레디스의 토큰을 정상적으로 삭제하는지 여부
# @pytest.mark.asyncio
# async def test_revoke_token(fastapi_client, idx_redis):
#     await createToken(testToken, 180, testUID, idx_redis)
#     response = fastapi_client.delete(f"/api/v1/auth/revoke/{testToken}")
#
#     assert response.status_code == 200
#     assert await findByToken(testToken, idx_redis) is False
#
#
# # 레디스에 없는 토큰을 삭제를 하더 라도 정상 작동하는지 확인
# @pytest.mark.asyncio
# async def test_revoke_token_fail(fastapi_client, idx_redis):
#     response = fastapi_client.delete(f"/api/v1/auth/revoke/{testFakeToken}")
#
#     assert response.status_code == 200
#     assert await findByToken(testToken, idx_redis) is False
