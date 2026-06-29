import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key="sk-6df1af5b69874d3a82651eacee3af239",
    base_url="https://api.deepseek.com"
)

def agent_jd_analyzer(jd):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": """你是一个岗位分析专家。
从岗位描述中提取以下信息，用结构化格式输出：
1. 必须技能（硬性要求）
2. 加分技能（优先要求）
3. 岗位核心职责（3条以内）
4. 隐含要求（从描述中推断出的潜在要求）"""},
            {"role": "user", "content": f"分析这个岗位：\n{jd}"}
        ]
    )
    return response.choices[0].message.content

def agent_resume_analyzer(resume, jd_analysis):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": """你是一个简历评估专家。
根据岗位分析结果，评估候选人简历，输出：
1. 匹配点（简历中符合岗位要求的部分）
2. 差距点（简历中缺失的岗位要求）
3. 亮点（简历中超出岗位要求的加分项）
4. 匹配度评分（0-100分）及理由"""},
            {"role": "user", "content": f"岗位要求分析：\n{jd_analysis}\n\n候选人简历：\n{resume}"}
        ]
    )
    return response.choices[0].message.content

def agent_interview_coach(jd_analysis, resume_analysis):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": """你是一个资深面试教练。
根据岗位分析和简历评估，生成针对性的面试准备建议：
1. 重点准备的技术问题（3个）及回答思路
2. 如何在面试中弥补差距点
3. 如何突出亮点和匹配点
4. 一句话总结：这个岗位值不值得投，胜算几何"""},
            {"role": "user", "content": f"岗位分析：\n{jd_analysis}\n\n简历评估：\n{resume_analysis}"}
        ]
    )
    return response.choices[0].message.content

# 页面设置
st.title("AI求职助手")
st.write("输入岗位JD和你的简历，三个AI Agent帮你分析匹配度和面试准备建议")

col1, col2 = st.columns(2)

with col1:
    jd = st.text_area("岗位描述（JD）", height=300, placeholder="粘贴岗位招聘描述...")

with col2:
    resume = st.text_area("你的简历", height=300, placeholder="粘贴你的简历内容...")

if st.button("开始分析"):
    if not jd or not resume:
        st.warning("请填写岗位描述和简历内容")
    else:
        with st.spinner("Agent1 正在分析岗位要求..."):
            jd_analysis = agent_jd_analyzer(jd)
        
        st.subheader("岗位分析结果")
        st.markdown(jd_analysis)
        st.divider()

        with st.spinner("Agent2 正在对比简历与岗位要求..."):
            resume_analysis = agent_resume_analyzer(resume, jd_analysis)
        
        st.subheader("简历匹配分析")
        st.markdown(resume_analysis)
        st.divider()

        with st.spinner("Agent3 正在生成面试建议..."):
            interview_advice = agent_interview_coach(jd_analysis, resume_analysis)
        
        st.subheader("面试准备建议")
        st.markdown(interview_advice)