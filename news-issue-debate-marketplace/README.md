# yul-plugins 마켓플레이스

Claude Code / Cowork 플러그인 마켓플레이스입니다. 현재는 플러그인 하나를
담고 있습니다.

## 포함된 플러그인

- **news-issue-debate** — 한국경제 뉴스에서 논쟁적인 쟁점을 뽑아 찬성/반대
  논거를 서로 다른 출처로 교차 검증해 중립적으로 정리해주는 플러그인.
  자세한 설명은 [plugins/news-issue-debate/README.md](plugins/news-issue-debate/README.md)
  참고.

## 사용자가 설치하는 방법

이 저장소가 GitHub 같은 곳에 올라가 있다면, Claude Code에서:

```
/plugin marketplace add <이 저장소의 owner>/<repo>
/plugin install news-issue-debate@yul-plugins
/reload-plugins
```

로컬 경로로 테스트하려면 저장소 경로를 그대로 씁니다:

```
/plugin marketplace add /path/to/news-issue-debate-marketplace
/plugin install news-issue-debate@yul-plugins
```

## 마켓플레이스 관리자(yul)를 위한 안내

### GitHub에 처음 올릴 때

로컬 PC(이 폴더가 있는 곳)에서:

```bash
cd news-issue-debate-marketplace
git init
git add .
git commit -m "Initial commit: news-issue-debate plugin"
```

그다음 GitHub에서 새 저장소를 만든 뒤(웹에서 만들거나 `gh repo create`),
그 저장소를 원격으로 등록하고 올립니다:

```bash
git remote add origin https://github.com/<본인 계정>/<repo 이름>.git
git branch -M main
git push -u origin main
```

### 나중에 플러그인을 업데이트할 때

`plugins/news-issue-debate/` 안의 파일을 수정한 뒤:

```bash
git add .
git commit -m "Update news-issue-debate"
git push
```

`marketplace.json`의 `plugins[].version`은 이 플러그인의
`.claude-plugin/plugin.json` 쪽에서 관리하니, 버전을 올릴 때는 그 파일의
`version` 값을 같이 올려주세요. 사용자는 `/plugin marketplace update`로
새 버전을 받아갑니다.

### 플러그인을 더 추가하고 싶을 때

`plugins/` 아래에 새 플러그인 폴더를 추가하고,
`.claude-plugin/marketplace.json`의 `plugins` 배열에 항목을 하나 더
넣으면 됩니다.
