import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key="sk-6df1af5b69874d3a82651eacee3af239",
    base_url="https://api.deepseek.com"
)

system_prompt = """
你是一位专业的简历优化顾问，拥有10年HR和猎头经验。

你的工作流程：
1. 用户发来简历内容后，先整体点评优缺点
2. 然后逐条给出具体修改建议
3. 对每一条经历，给出修改前和修改后的对比
4. 用数据和动词强化描述，比如"负责项目"改成"主导3人团队完成XX项目，效率提升40%"
"""

st.title("简历优化助手")
st.write("把你的简历内容粘贴进来，AI帮你优化")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

if user_input := st.chat_input("粘贴你的简历内容..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)