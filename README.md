# KAIST EMC Lab 홈페이지

서버나 빌드 도구가 필요 없는 정적 홈페이지입니다. 실제 인물·논문·프로젝트·뉴스와 연락처는 검증 후 입력하도록 비워 두었습니다. 시각 요소는 자체 제작했으며 공식 KAIST 로고나 참고 사이트의 이미지를 사용하지 않습니다.

## 폴더 구조

```text
index.html, professor.html, members.html, research.html
publications.html, projects.html, news.html, contact.html
assets/style.css       디자인 및 반응형 스타일
assets/app.js          페이지 내용, 데이터 표시, 검색 및 필터
assets/images/         선택 사항: 사용 권한이 있는 사진 저장
 data/members.json     구성원
 data/publications.json 논문 및 특허
 data/projects.json    프로젝트
 data/news.json        뉴스
```

## 로컬에서 실행하기

`index.html`을 더블 클릭하면 브라우저의 보안 정책 때문에 JSON을 불러오지 못할 수 있습니다. 이 폴더에서 터미널을 열고 Python이 설치되어 있다면 다음을 실행하세요.

```sh
python -m http.server 8000
```

브라우저에서 `http://localhost:8000/`을 엽니다. 종료는 터미널에서 Ctrl+C를 누릅니다. Python이 없다면 VS Code의 Live Server 같은 정적 서버를 사용할 수 있습니다.

## 콘텐츠 수정

`data` 폴더의 JSON 파일을 텍스트 편집기나 GitHub 웹 편집기에서 수정합니다. 각 파일은 배열이며, 항목 사이에 쉼표가 필요하고 마지막 항목 뒤에는 쉼표를 넣지 않습니다. 문자열 안의 큰따옴표는 `\"`로 입력합니다. 아래는 형식 예시이며 실제 정보가 아닙니다. 예시를 복사한 뒤 검증된 정보로 바꾸세요.

`members.json`:
```json
[{"group":"Ph.D. Students","name":"이름","degree":"Ph.D. Student","research":"연구 분야","email":"name@example.com","photo":"assets/images/member.jpg"}]
```
`group`은 `Professor`, `Ph.D. Students`, `M.S. Students`, `Alumni` 중 하나입니다. 사진이 없으면 `photo`를 비워 두세요. 사진은 사용 권한과 본인 동의를 확인한 뒤 `assets/images`에 넣으세요.

`publications.json`:
```json
[{"type":"International Journal Papers","title":"논문 제목","authors":"저자","venue":"학술지 또는 학회","year":2025,"doi":"10.1234/example"}]
```
`type`은 `International Journal Papers`, `International Conference Papers`, `Domestic Publications`, `Patents` 중 하나입니다. DOI는 없으면 빈 문자열로 둡니다. 검색은 제목·저자·학술지·DOI를 대상으로 하며 연도 및 분류 필터와 함께 동작합니다.

`projects.json`:
```json
[{"status":"Ongoing Projects","title":"프로젝트명","period":"2025–2027","description":"연구 내용","institution":"관련 기관"}]
```
`status`는 `Ongoing Projects` 또는 `Completed Projects`입니다.

`news.json`:
```json
[{"date":"2025-03-01","category":"AWARD","title":"소식 제목","summary":"소식 요약","url":""}]
```
날짜는 `YYYY-MM-DD`로 입력합니다. 메인 페이지에는 날짜순 최신 3건이 표시됩니다. 외부 링크가 없으면 `url`을 비워 두세요. JSON 파일 저장 후 새로고침합니다. 사이트는 HTML 코드 실행을 막기 위해 데이터의 텍스트를 이스케이프합니다. JSON은 GitHub에서 공개되므로 비밀번호, API 키, 개인 정보를 넣지 마세요.

교수 약력, 연구 분야 설명, 주소 및 지원 안내는 `assets/app.js`의 해당 페이지 부분을 수정합니다. 실제 건물과 호실, 연락처를 확인한 뒤 Contact 페이지를 완성하세요. 현재 지도 링크는 KAIST 전체 위치를 가리키며 연구실 위치를 의미하지 않습니다. 필요에 따라 JSON 기반 CMS를 추가할 수 있습니다.

## GitHub Pages 배포

1. GitHub에서 새 저장소를 만들고 이 폴더 안의 파일과 `assets`, `data` 폴더를 저장소 최상위에 업로드합니다. `index.html`이 최상위에 있어야 합니다.
2. 저장소의 **Settings → Pages**에서 **Build and deployment → Source**를 **Deploy from a branch**로 선택합니다.
3. 기본 브랜치(보통 `main`)와 `/ (root)`를 선택하고 **Save**를 누릅니다.
4. 배포가 완료되면 Pages 설정에 표시되는 `https://사용자명.github.io/저장소명/` 주소로 접속합니다. 상대 경로를 사용하므로 프로젝트 하위 경로에서도 작동합니다. GitHub Pages의 HTTPS 설정을 확인하세요.
5. 이후 GitHub에서 JSON을 편집하고 **Commit changes**를 누르면 Pages가 다시 배포됩니다. 반영까지 시간이 걸릴 수 있습니다.

공개 전 실제 자료, 이미지 권리, 연락처 및 개인정보를 확인하세요. 외부 Google Fonts에 접속할 수 없으면 시스템 글꼴로 표시됩니다.
