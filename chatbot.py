import tkinter as tk
import urllib3
import json
from tkinter import messagebox

# ETRI API 설정
openApiURL = "http://aiopen.etri.re.kr:8000/WiseQAnal"
accessKey = "074c136c-f5d7-4063-811b-9cf8b8060803"

# 병원 관련 질문-답변 세트
hospital_questions = {
    "진료 시간": "병원의 진료 시간은 오전 9시부터 오후 6시까지입니다.",
    "응급실 위치": "응급실은 본관 1층에 위치하고 있습니다.",
    "의사 정보": "내과의 김철수 의사, 소아과의 박영희 의사가 있습니다."
}

# ETRI API 응답 함수
def get_response(question):
    requestJson = {
        "access_key": accessKey,  # API 키를 요청 본문에 포함
        "argument": {
            "text": question,
            "analysis_code": "QA"
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )
    return json.loads(response.data.decode('utf-8'))

def send_message(event=None):
    user_question = preprocess_question(user_input.get().strip())  # 사용자 입력을 전처리
    chat_box.config(state=tk.NORMAL)
    
    if user_question:  # 입력이 공백이 아닌 경우에만 처리
        chat_box.insert(tk.END, f"사용자: {user_input.get().strip()}\n\n", "user")
        user_input.delete(0, tk.END)  # 입력 필드를 비움

        # 키워드 기반 매칭 추가
        if "진료" in user_question and "시간" in user_question:
            chat_box.insert(tk.END, "챗봇: 병원의 진료 시간은 오전 9시부터 오후 6시까지입니다.\n\n", "bot")
        elif "응급실" in user_question and "위치" in user_question:
            chat_box.insert(tk.END, "챗봇: 응급실은 본관 1층에 위치하고 있습니다.\n\n", "bot")
        elif "진료" in user_question:  # 단일 키워드 "진료"만 들어왔을 때
            chat_box.insert(tk.END, "챗봇: 병원의 진료는 예약제로 운영됩니다. 자세한 정보는 병원 홈페이지를 참고해 주세요.\n\n", "bot")
        elif "시간" in user_question:  # 단일 키워드 "시간"만 들어왔을 때
            chat_box.insert(tk.END, "챗봇: 병원의 운영 시간은 오전 9시부터 오후 6시까지입니다.\n\n", "bot")
        elif "위치" in user_question:  # 단일 키워드 "위치"만 들어왔을 때
            chat_box.insert(tk.END, "챗봇: 병원은 서울시 강남구에 위치해 있습니다.\n\n", "bot")
        else:
            result = get_response(user_question)
            # API 호출 결과를 확인하고 답변 출력
            answer = result.get('return_object', {}).get('answer', '관련 정보를 찾을 수 없습니다.')
            chat_box.insert(tk.END, f"챗봇: {answer}\n\n", "bot")

    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)  # 스크롤을 자동으로 아래로 내림


def preprocess_question(question):
    # 질문에서 공백 제거 및 소문자 변환 등의 전처리 작업
    return question.replace(" ", "").strip().lower()


# GUI 설정
root = tk.Tk()
root.title("병원 챗봇")
root.geometry("600x700")
root.configure(bg="#f0f0f0")

# 채팅창 스타일
chat_box = tk.Text(root, state=tk.DISABLED, height=30, width=55, padx=10, pady=10, wrap=tk.WORD, bg="#ffffff", fg="#000000", font=("Helvetica", 12))
chat_box.tag_configure("user", foreground="#1a73e8")
chat_box.tag_configure("bot", foreground="#34a853")
chat_box.pack(pady=20)

# 입력 필드와 전송 버튼 스타일
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10)

user_input = tk.Entry(input_frame, width=40, font=("Helvetica", 12))
user_input.grid(row=0, column=0, padx=10)

send_button = tk.Button(input_frame, text="전송", command=send_message, bg="#1a73e8", fg="white", font=("Helvetica", 12, "bold"))
send_button.grid(row=0, column=1)

# 엔터키로 전송 기능
user_input.bind("<Return>", send_message)

# Tkinter 메인 루프
root.mainloop()


st.hospital_chatbot()
