# KAIST EMC Lab 홈페이지 관리

이 홈페이지는 GitHub Pages와 Jekyll을 사용하는 정적 사이트입니다. 현재 디자인은 GitHub에 저장된 버전을 기준으로 합니다. 본문과 검색은 JavaScript, 공통 머리글과 바닥글은 Jekyll이 처리합니다. 서버와 데이터베이스를 별도로 운영하지 않습니다.

## 시작하기

이 폴더에서 다음을 실행한 뒤 `http://127.0.0.1:8001/`을 엽니다. `Ctrl+C`로 종료합니다.

```sh
python scripts/preview.py
```

미리보기는 이 프로젝트에 필요한 템플릿만 처리하며 실제 Jekyll을 대체하지 않습니다. GitHub에 올리면 Actions에서 실제 Jekyll 빌드와 콘텐츠 검사를 실행하도록 준비되어 있습니다. GitHub Actions가 실행되는지는 저장소 설정에 따릅니다. `index.html`을 직접 열거나 일반 `python -m http.server`를 사용하면 Jekyll 템플릿이 렌더링되지 않습니다.

## 콘텐츠 관리

- 논문·특허: `_data/publications/` 안에 **한 건당 JSON 파일 하나**
- 뉴스: `_data/news/` 안에 **한 건당 JSON 파일 하나**
- 구성원: `data/members.json`
- 프로젝트: `data/projects.json`
- 공지 팝업: `data/announcement.json`

논문과 뉴스 폴더는 현재 비어 있습니다. 실제 자료를 검증한 후 입력하세요. 아래는 형식을 설명하는 예시이며 실제 연구실 실적이 아닙니다.

논문 파일 예시 (`_data/publications/paper-2025-01.json`):

```json
{"title":"논문 제목","authors":"저자","venue":"학술지","year":2025,"type":"International Journal Papers","doi":"10.1234/example"}
```

분류는 `International Journal Papers`, `International Conference Papers`, `Domestic Publications`, `Patents` 중 하나입니다. DOI가 없다면 빈 문자열로 둡니다.

뉴스 파일 예시 (`_data/news/news-2025-01.json`):

```json
{"date":"2025-03-01","category":"NEWS","title":"소식 제목","summary":"소식 요약","url":""}
```

날짜는 `YYYY-MM-DD`입니다. 뉴스는 날짜순으로 정렬되며 최신 3건이 메인 화면에 표시됩니다. 외부 링크는 `https://`로 시작하는 주소 또는 빈 문자열을 사용합니다. 자료를 추가한 뒤 아래 검사에서 오류가 없는지 확인하세요.

```sh
python scripts/validate_content.py
python -m unittest discover -s tests -v
```

`data/publications.json`과 `data/news.json`은 Jekyll이 별도 파일을 모아서 생성하는 출력 템플릿입니다. **이 두 파일에 직접 자료를 입력하지 마세요.** 미리보기 도구도 동일한 자료 폴더를 읽습니다. 현재 검색은 모든 논문 메타데이터를 한 번에 읽어 브라우저에서 처리합니다. 자료가 많아져 실제로 느려지면 검색 인덱스·페이지 나누기를 추가해야 합니다.

### 공지 팝업

`data/announcement.json`에서 `enabled`, `title`, `message`를 수정합니다. 현재 문구는 기능 확인용이므로 실제 공지로 교체하세요. 새 공지를 이전에 닫은 방문자에게 다시 표시하려면 `id`를 변경합니다. `dismiss_hours`는 다시 보지 않기 시간(1~720시간)입니다. 일반 닫기와 Escape는 해당 창만 닫습니다. 링크가 필요하면 `link_text`, `link_url`을 함께 입력합니다. 끄려면 `enabled`를 `false`로 설정합니다.

### Pages CMS 설정

`.pages.yml`은 논문·뉴스 항목별 입력 화면과 구성원·프로젝트·공지 파일을 위한 **설정 파일**입니다. 아직 Pages CMS 서비스 연결이나 GitHub 앱 설치는 하지 않았습니다. 실제 사용 전 GitHub 저장소에 변경사항을 올리고 [Pages CMS](https://pagescms.org/docs/quick-start/)에서 GitHub 계정으로 로그인하여 해당 저장소에만 필요한 권한을 부여한 뒤, 각 입력·저장·배포 과정을 시험해야 합니다. 이 설정은 실제 서비스에서 아직 검증되지 않았습니다. 저장소에 올린 정보는 공개 범위에 따라 다른 사람이 볼 수 있습니다. 개인정보나 비밀키는 올리지 마세요.

## 백업

```sh
python scripts/backup.py
```

`.backups`에 날짜가 포함된 ZIP을 만듭니다. 이 ZIP은 현재 소스 파일의 **스냅샷**이고 Git 변경 이력은 포함하지 않습니다. 파일을 학교에서 승인한 독립 저장소에 복사하고, 주기적으로 다른 폴더에 압축을 풀어 미리보기가 실행되는지 시험하세요. 기존 `.previous-local-design`은 이전 로컬 디자인 백업이며 이 스냅샷에 포함하지 않습니다. Git 이력이 있는 실제 저장소를 복제해 사용한다면 별도로 Git 전체 이력도 보관하세요.

## GitHub Pages 배포

`_config.yml`, `_layouts`, `_data`, `.github`, `.pages.yml`, `Gemfile`, `assets`, `data`, 모든 HTML, `scripts`, `tests`를 저장소에 반영하고 Pages 배포 소스를 브랜치의 루트로 설정합니다. `.nojekyll`을 추가하면 Jekyll 처리와 자료 생성이 작동하지 않습니다. `_data`와 `_layouts`는 폴더 이름 앞의 밑줄이 필수입니다. 배포 후 Actions의 검사와 실제 홈페이지의 연구·논문 검색·뉴스·공지 표시를 확인합니다. 현재 로컬 작업과 GitHub 저장소는 자동 동기화되지 않습니다.

운영·인수인계 계획은 [docs/OPERATIONS.md](docs/OPERATIONS.md)를 참고하세요.
