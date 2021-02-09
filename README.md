# ScenarioEditor

## 실행방법

  ```
  # Set input parameters in ScenarioEditor_options.py
  # run ScenarioEditor
  python ScenarioEditor.py
  ```

## 사용법

- 액션 스크립트 로드 : 시나리오 에디터 실행 전 ./data 폴더에 스크립트 db 파일을 넣어둔다. 시나리오 에디터 실행 후 왼쪽 상단 액션 스크립트 로드 버튼을 클릭하여 해당 db 파일을 연다.

- 카테고리 선택 : 스크립트 로드 후, 왼쪽 테이블에 해당 db의 카테고리 목록이 뜬다. 이 목록의 체크 박스를 클릭하여 선택/해제를 할 수 있다. 또한, Drag & Drop으로 카테고리의 순서를 변경 할수 있다.

- 액션 스크립트 선택 : 카테고리를 클릭하면 해당 액션 스크립트 목록이 뜬다. 액션 스크립트 목록 또한 체크 박스를 클릭하여 선택/해제 할 수 있으며 Drag & Drop으로 순서 변경이 가능하다.

- 제목 입력: 상단 중앙부의 텍스트박스에 제목을 입력할 수 있다.

- 기타 : 일반모드/영상모드, 세로모드/가로모드, 테마1~3 선택이 가능하다. 

- Export : 위에서 선택한 정보를 바탕으로 json 형태로 파일을 생성한다. 구조는 아래와 같다.

- 예시

```
{
  "Categories": [
    "시설안내",
    "박물관소개"
  ],
  "ActionScript": [
    {
      "Name": [
        "am-space-01.json",
        "am-space-02.json"
      ],
      "Category": "시설안내"
    },
    {
      "Name": [
        "am-intro-01.json",
        "am-intro-02.json"
      ],
      "Category": "박물관소개"
    }
  ],
  "PlayMode": "Interactive",
  "Layout": "Horizontal",
  "Theme": "1",
  "Title": "박물관 소개"
}
```
