<p align="center"><img src="./cover.png" width="100%" /></p>

<h1 align="center">agent-handoff-skill</h1>
<p align="center">
  <em>새 에이전트가 전체 세션을 다시 읽지 않고도 바로 이어받을 수 있도록 continuation-ready HANDOFF.md를 만드는 HANDOFF 스킬의 공개 패키징 저장소입니다.</em>
</p>
<p align="center">
  <a href="#빠른-시작">빠른 시작</a> · <a href="#무엇이-포함되나">무엇이 포함되나</a> · <a href="#동작-방식">동작 방식</a> · <a href="./README.md">English</a>
</p>

---

> [!NOTE]
> 이 저장소는 `handoff` 스킬의 핵심 매니페스트, canonical 템플릿, 이중 언어 문서, 재현 가능한 cover asset을 함께 패키징합니다. `examples/`와 `evals/`는 public-safety와 public-value 검토를 통과한 경우에만 포함됩니다.

## 문제 정의

대부분의 세션 요약은 changelog처럼 작성됩니다. 무엇이 있었는지는 말해주지만, 새 에이전트가 어디서부터 다시 시작해야 하는지는 충분히 알려주지 못합니다. HANDOFF 스킬은 더 좁고 실용적인 문제를 해결합니다. 즉, 작업 중단 지점, 완료된 일, 실패한 시도, 남은 작업, 검증 방법을 한 문서로 정리해 **재시작 가능성**을 높입니다.

## 무엇이 포함되나

### 필수 구성

- `SKILL.md` — 스킬 매니페스트와 운영 계약
- `templates/HANDOFF.md` — canonical HANDOFF 구조
- `README.md` / `README-Ko-KR.md` — 공개용 문서
- `generate_cover.py` / `cover.png` — 재현 가능한 cover asset pair
- `LICENSE` / `.gitignore`

### 선택적 품질 자산

이 저장소에 아래가 있다면 의도적으로 포함된 것입니다.

- `examples/` — 출력 품질을 보여주는 generic 예시
- `evals/` — 품질 기대치를 보존하는 public-safe eval 케이스

## 빠른 시작

### 복사-붙여넣기 설치

```text
handoff skill을 설치해 줘. 아래 단계대로 실행해:
1. TMP_DIR=$(mktemp -d)
2. git clone https://github.com/wjgoarxiv/agent-handoff-skill.git "$TMP_DIR/agent-handoff-skill"
3. mkdir -p ~/.claude/skills/handoff
4. cp -r "$TMP_DIR/agent-handoff-skill/SKILL.md" "$TMP_DIR/agent-handoff-skill/templates" ~/.claude/skills/handoff/
5. "$TMP_DIR/agent-handoff-skill/examples" 가 있으면 함께 복사해 줘.
6. "$TMP_DIR/agent-handoff-skill/evals" 가 있으면 함께 복사해 줘.
7. "handoff skill 설치 완료"라고 말해 줘
```

### 수동 설치

```bash
TMP_DIR=$(mktemp -d)
git clone https://github.com/wjgoarxiv/agent-handoff-skill.git "$TMP_DIR/agent-handoff-skill"
cd "$TMP_DIR/agent-handoff-skill"

mkdir -p ~/.claude/skills/handoff
cp -r SKILL.md templates ~/.claude/skills/handoff/

# 선택적 품질 자산
[ -d examples ] && cp -r examples ~/.claude/skills/handoff/
[ -d evals ] && cp -r evals ~/.claude/skills/handoff/
```

### 기타 도구

| 도구 | 스킬 경로 | 설치 패턴 |
|------|----------|-----------|
| **Claude Code** | `~/.claude/skills/handoff/` | `SKILL.md` + `templates/` 복사 |
| **Codex CLI** | `~/.codex/skills/handoff/` | 동일한 shipped asset을 Codex skills 디렉터리에 복사 |
| **Gemini CLI** | `~/.gemini/skills/handoff/` | 동일한 shipped asset을 Gemini skills 디렉터리에 복사 |

## 사용 예시

### 1. 컨텍스트 윈도우가 거의 찼을 때

```text
컨텍스트를 잃기 전에 지금 진행 중인 작업을 handoff로 정리해 줘.
```

### 2. 작업이 막혀서 다른 에이전트로 넘겨야 할 때

```text
새 에이전트가 이 실패를 이어서 디버깅할 수 있도록 HANDOFF.md를 작성해 줘.
```

### 3. 장기 작업을 깔끔한 재시작 지점으로 남기고 싶을 때

```text
현재 상태를 changelog가 아니라 continuation-ready handoff로 정리해 줘.
```

위 프롬프트는 의도적으로 짧습니다. 구조는 스킬이 결정하므로, 작성자는 fresh-agent handoff가 필요하다는 사실만 명확히 전달하면 됩니다.

## 동작 방식

```text
            handoff skill flow
            ~~~~~~~~~~~~~~~~~~

  [진행 중인 작업]
          |
          v
  +-----------------------+
  | 1. 필요성 판단        |
  | 컨텍스트 부족? block? |
  | transition 필요?      |
  +-----------------------+
          |
          v
  +-----------------------+
  | 2. 근거 수집          |
  | 파일 / 명령 / 커밋 /  |
  | 에러 출력             |
  +-----------------------+
          |
          v
  +-----------------------+
  | 3. HANDOFF.md 작성    |
  | 필수 섹션 기준        |
  | 순서 준수             |
  +-----------------------+
          |
          v
  +-----------------------+
  | 4. 재시작 가능성 점검 |
  | 새 에이전트가         |
  | 바로 재개 가능한가?   |
  +-----------------------+
```

## 출력 형식

생성되는 `HANDOFF.md`는 항상 다음 섹션을 이 순서대로 포함해야 합니다.

1. `Task`
2. `Current State`
3. `What Was Done`
4. `Key Decisions`
5. `Open Issues`
6. `Next Steps`
7. `Context for Continuation`

`Verification Commands`, `Key Files`, `Evidence & References` 같은 supplementary section은 다음 에이전트의 실행에 실제로 도움이 될 때만 포함합니다.

## 저장소 구조

```text
agent-handoff-skill/
├── SKILL.md
├── README.md
├── README-Ko-KR.md
├── LICENSE
├── .gitignore
├── generate_cover.py
├── cover.png
├── templates/
│   └── HANDOFF.md
├── examples/                 # optional, review 통과 시에만 포함
│   └── HANDOFF-example-generic-auth-refactor.md
└── evals/                    # optional, review 통과 시에만 포함
    └── evals.json
```

## Public Packaging 메모

- 이 저장소는 스킬 패키징용입니다. 실제 runtime 산출물은 항상 `<active-project-root>/HANDOFF.md`에 작성됩니다.
- 템플릿은 reference asset이며, runtime output 위치가 아닙니다.
- `examples/`와 `evals/`가 포함되어 있다면 generic/public-safe 기준을 통과했기 때문입니다.

## 라이선스

이 프로젝트는 [MIT License](./LICENSE)를 따릅니다.
