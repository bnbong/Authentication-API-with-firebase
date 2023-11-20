# Authentication API with firebase

파이어베이스 기반의 인증 API 입니다.

파이어베이스의 API를 사용해 사용자를 인증하고, 해당 파이어베이스 토큰의 유효기간 만큼 레디스에 인증 정보를 저장하여, 파이어베이스의 API의 호출 없이 레디스의 데이터 확인만으로 사용자를 인증할 수 있도록합니다(토큰 캐싱 저장 기능은 구현중).

자람 학회의 "자람 허브" 스터디 "msng(마쉿는거)" 프로젝트에서 임시로 사용할 인증 API로 개발되었습니다.

**임시 유저 인증 API이기 때문에 실제 자람 허브 DB의 유저 정보와 검증하는 로직은 생략되어 있으며, 추후 업데이트를 통해 추가하거나 인증 API 서비스 자체가 삭제될 수 있습니다.**

## 인증 Flow

1. 사용자는 다음 url을 통해 로그인을 할 수 있습니다 : `GET /api/v1/auth/login`
2. 상단의 url로 들어가면 구글 로그인 페이지(OAuth)로 리다이렉트 되어 로그인을 시도합니다.
3. 이때, 로그인한 구글 로그인 계정이 jaram-groupware의 firebase app의 사용자로 등록이 되어 있다면 로그인이 성공하고, 해당 사용자의 firebase 토큰을 발급받습니다.
4. 로그인 과정이 모두 정상적으로 수행이 되면 리다이렉션한 `GET /api/v1/auth/auth`페이지에서 Firebase ID token을 볼 수 있습니다.

## 개발 Stack
- Python 3.10.10
- FastAPI 0.104.1
- firebase-admin 6.2.0
- Redis 5.0.5-alpine
- MariaDB 10.5.8 (for testing)
- Docker 24.0.2, Docker Compose 2.18.1

## 내부 로직 Flow 개요

Jaram Groupware의 firebase application은 Google OAuth2.0 클라이언트, Github OAuth2.0 클라이언트를 통해 소셜 로그인을 수행합니다.

해당 프로젝트에서 구현한 파이어베이스 인증 API는 연결된 Google OAuth2.0 클라이언트만을 사용해서 구글 로그인만 수행할 수 있는 서비스입니다.

연결된 Google OAuth2.0 클라이언트에서 등록되어 있는 리다리엑션 URI를 포함하여 클라이언트 및 정보를 받아올 scope 내용을 google OAuth2.0 인증 API에 전달하면,
Google OAuth2.0 웹 클라이언트가 리다이렉션 URI로 소셜 로그인한 유저 정보가 담긴 `ID token`을 전달합니다.

**그러나, 해당 `ID token`은 Firebase 앱에서 받아온 정보가 아니기 때문에 여기서 받아온 `ID token`은 Firebase에서 바로 사용할 수 없습니다.**

따라서, 현재 파이어베이스 인증 API는 Google에서 받아온 `ID token`을 바탕으로 해당 유저의 이메일 해석하여 파이어베이스 앱에 저장되어 있는 유저의 이메일과 비교하여, 검색합니다.

만약, 해당 이메일이 파이어베이스 앱에 등록되어 있다면, 해당 유저의 UID를 바탕으로 custom_token을 발급합니다.

Firebase custom token이 정상적으로 발급이 되었다면, 해당 custom token을 바탕으로 Firebase `ID token`을 최종적으로 발급받습니다.

여기서 발급된 `ID token`이 비로소 Firebase의 ID Token 이 됩니다.

## 참고한 References

- [Firebase Admin SDK 공식 문서](https://firebase.google.com/docs/admin/setup?hl=ko)
- [firebase-admin의 auth 모듈 공식 문서](https://firebase.google.com/docs/reference/admin/python/firebase_admin.auth)
- [firebase-admin유용한 명령어 모음](https://negabaro.github.io/archive/useful-firebase_admin-command)
