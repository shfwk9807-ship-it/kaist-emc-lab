# 장기 운영 및 인수인계

## 현재 상태

- 기준 저장소는 개인 계정 `shfwk9807-ship-it/kaist-emc-lab`입니다. 연구실 조직은 아직 없으며 이 문서 작성 시점에 이전하지 않았습니다.
- Pages CMS 설정은 로컬에 준비되어 있지만 서비스 연결, 인증, 권한 부여는 아직 하지 않았습니다.
- GitHub Actions의 실제 Jekyll 빌드 결과와 CMS 서비스 연결 후 편집·배포 결과를 확인해야 합니다.

## 조직 소유권

1. 연구실이 관리할 GitHub 조직의 이름, 이메일, 소유자 2명 이상, 2단계 인증과 복구 방법을 정합니다. 구성원은 공용 비밀번호 대신 개인 계정을 사용합니다.
2. 새 조직과 소유자 권한을 확인하고 현 소유자와 조직의 이전 권한을 확인합니다.
3. 저장소 이전 전에 현재 GitHub Pages 주소, 도메인, GitHub 앱·CMS 연동, Pages 설정을 기록하고 백업합니다. 실제 이전은 수신 조직과 사용자 승인 후 진행합니다.
4. GitHub Pages 주소가 바뀔 수 있고 GitHub는 기존 Pages 주소를 자동으로 새 주소에 연결하지 않습니다. 새 URL, 링크와 접근 권한을 검증합니다. 학교 도메인은 해당 부서에 소유권, DNS, 갱신 절차를 문의합니다.
5. 새 담당자의 편집·배포를 직접 시험한 뒤 기존 담당자의 불필요한 권한과 연결을 철회합니다. 후임 소유자를 먼저 확보합니다.

## 정기 관리

- 논문·뉴스는 건별 파일이나 승인된 CMS에서 작성하고 공개 정보와 사용 권한을 확인합니다. DOI 및 링크는 원본과 대조합니다.
- 콘텐츠 검사와 Actions 빌드가 성공했는지 확인하고 공개 페이지에서 검색·연도 필터, 뉴스, 공지를 점검합니다.
- 사진·문서·영상의 사용 권한과 보관 비용을 확인합니다. 대용량 자료는 GitHub Pages 한도 및 기관 정책에 맞는 별도 보관소를 사용합니다.
- 소스 ZIP과 Git 이력을 독립된 승인 저장소에 정기적으로 보관합니다. 복원 시험 및 담당자를 정해 기록합니다. 이 저장소의 `.backups`는 같은 컴퓨터에 있으므로 독립 백업이 아닙니다.
- GitHub 조직 소유자·CMS 권한·2단계 인증 복구수단, 도메인 소유권과 만료일을 정기 확인합니다. GitHub 및 CMS 서비스 정책과 한도는 바뀔 수 있습니다.
- 자료량이 커지면 실제 검색 속도와 파일 크기를 측정한 뒤 연도별 분할, 페이지 나누기 또는 별도 검색 인덱스를 도입합니다. 현재는 전체 메타데이터를 브라우저로 전송합니다.

## 복원 시험

1. 독립 저장소에 보관한 ZIP을 새 폴더에 풉니다. 압축 경로가 예상 폴더 안에 있는지 확인합니다.
2. `python scripts/validate_content.py`와 `python -m unittest discover -s tests -v`를 실행합니다.
3. `python scripts/preview.py`로 메인·공지·논문 검색·뉴스·구성원 페이지를 확인합니다.
4. GitHub Pages 호환 Ruby/Jekyll 환경에서 `bundle install`, `bundle exec jekyll build`를 실행하고 생성된 `_site`의 JSON과 페이지를 확인합니다.
5. Git 이력 복원이 필요하면 별도 보관한 Git 저장소 또는 bundle도 복원합니다. ZIP에는 커밋 이력이 없습니다.

관련 문서: [GitHub 조직 소유권 유지](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/maintaining-ownership-continuity-for-your-organization), [저장소 이전](https://docs.github.com/en/repositories/creating-and-managing-repositories/transferring-a-repository), [Pages CMS 시작](https://pagescms.org/docs/quick-start/), [GitHub Pages 한도](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).
