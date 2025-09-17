from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# LLM呼び出し
def get_llm_response(user_input: str, expert_type: str) -> str:

    # 専門家ごとにシステムメッセージを切り替え
    if expert_type == "カメラマン":
        system_prompt = "あなたは優秀なカメラマンです。写真撮影に関する専門的な視点で回答してください。"
    elif expert_type == "家庭料理のプロ":
        system_prompt = "あなたは家庭料理のプロです。料理に関する専門的な視点で回答してください。"
    else:
        system_prompt = "あなたはアシスタントです。"

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]

    result = llm(messages)
    return result.content


# ====== Streamlit アプリ部分 ======
st.title("専門家チャット")

st.write("""
このアプリは、入力したテキストに対して回答します。  
ラジオボタンで「カメラマン」または「家庭料理のプロ」を選ぶと、それぞれの専門家としての観点で回答が得られます。  

### 操作方法
1. 専門家の種類を選択してください  
2. テキストを入力してください  
3. 「実行」ボタンを押すと、LLMからの回答が表示されます
""")

# 専門家の種類を選択
selected_expert = st.radio(
    "専門家の種類を選んでください。",
    ["カメラマン", "家庭料理のプロ"]
)

# 入力フォーム
user_text = st.text_area("相談したい内容や質問を入力してください。", height=100)

# 実行ボタン
if st.button("実行"):
    if user_text.strip():
        with st.spinner("問い合わせ中..."):
            response = get_llm_response(user_text, selected_expert)
        st.divider()
        st.write("### 回答")
        st.success(response)
    else:
        st.error("入力テキストを入力してから実行してください。")
