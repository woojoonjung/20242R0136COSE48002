# Dr.Snap
COSE480-02 Capston Design Project   
   
> 닥터스냅(Dr.Snap)은 이미지 기반의 피부질환 진단 챗봇서비스입니다.   
> 시공간적 제약이 많은 현대인들이 자신의 병변을 대수롭지 않게 여기고   
> 병원 방문을 미루는 경향을 보이고 현재 비대면 진료 플랫폼들이 가지는   
> 몇 가지 페인포인트들에 주목하여 서비스를 기획 및 개발하게 되었습니다.   
> 의사들이 직접 답변을 작성하는 기존의 비대면 진료 서비스와 달리   
> LLM을 활용한 더 즉각적인 상호작용(질문과 답변)과   
> 뛰어난 접근성을 가진 나만의 피부과 전문의, 닥터스냅을 제안합니다.

### 요구사항
requirements.txt의 패키지를 다음 스크립트를 실행하여 설치하시기 바랍니다.   
```sh
pip install -r requirements.txt   
```
   
다음으로 프로젝트를 실행하는 로컬 환경에 맞게 다음 파일의 API_URL을 설정해야 합니다.   
> frontend/dr-snap/src/services/api.jsx   
   
마지막으로 console.cloud.google.com 에 접속하여 Cloud Vision API와   
openAI의 API에 대한 권한과 API키를 취득한 후 .env파일을 구성해주세요.   
후에 .env 파일은 다음 위치에 저장해주세요.   
> backend/ml/rag
      
### 사용법
다음 스크립트를 통해 백엔드 서버를 실행해주세요.   
```sh
cd backend   
python __main__.py   
```
   
다음 스크립트를 실행한 후 연결된 포트 번호에 따라 브라우저에 주소를 입력해 클라이언트에 접속해주세요 (e.g. https://localhost:5173)   
```sh
cd frontend   
npm run dev   
```
   
Enjoy! 🙂