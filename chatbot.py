import urllib3
import json

openApiURL = "http://aiopen.etri.re.kr:8000/WiseQAnal"
accessKey = "074c136c-f5d7-4063-811b-9cf8b8060803"  # API Key 설정
a = [1,2,3]
hospital_questions = {
    "a": a[0], # 이런식으로 리스트로 만들어서 할 거임
    "진료 시간": "병원의 진료 시간은 오전 9시부터 오후 6시까지입니다.",
    "응급실 위치": "응급실은 본관 1층에 위치하고 있습니다.",
    "의사 정보": "내과의 김철수 의사, 소아과의 박영희 의사가 있습니다."
}

def get_response(question):
    requestJson = {
        "argument": {
            "text": question
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey},
        body=json.dumps(requestJson)
    )
    return json.loads(response.data.decode('utf-8'))

def hospital_chatbot():
    while True:
        user_question = input("사용자: ")
        if user_question.lower() == '종료':
            print("챗봇: 대화를 종료합니다.")
            break

        # ETRI API 호출하여 질문 분석
        result = get_response(user_question)

        # 질문에 대한 대답을 미리 정의된 질문과 매칭
        for question, answer in hospital_questions.items():
            if question in user_question:
                print(f"챗봇: {answer}")
                break
        else:
            print("챗봇: 죄송합니다, 관련 정보를 찾을 수 없습니다.")

st.hospital_chatbot()
