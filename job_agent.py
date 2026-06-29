from openai import OpenAI

client = OpenAI(
    api_key="sk-6df1af5b69874d3a82651eacee3af239",
    base_url="https://api.deepseek.com"
)

def agent_jd_analyzer(jd):
    """Agent1：分析岗位JD，提取核心要求"""
    print(">>> Agent1 正在分析岗位要求...")
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
    """Agent2：对比简历和JD，找出匹配点和差距"""
    print(">>> Agent2 正在对比简历与岗位要求...")
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
    """Agent3：根据分析结果生成面试准备建议"""
    print(">>> Agent3 正在生成面试准备建议...")
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

def run_job_agent(jd, resume):
    print("\n===== AI求职助手启动 =====\n")
    
    # 三个Agent依次执行
    jd_analysis = agent_jd_analyzer(jd)
    print(f"\n【岗位分析结果】\n{jd_analysis}\n")
    
    resume_analysis = agent_resume_analyzer(resume, jd_analysis)
    print(f"\n【简历匹配分析】\n{resume_analysis}\n")
    
    interview_advice = agent_interview_coach(jd_analysis, resume_analysis)
    print(f"\n【面试准备建议】\n{interview_advice}\n")
    
    print("===== 分析完成 =====")

# 测试数据
jd = """
岗位：AI应用开发工程师
职责：
- 基于大语言模型开发AI应用
- 设计和实现RAG知识库系统
- 开发和维护AI Agent系统
要求：
- 熟悉Python编程
- 了解LangChain、LlamaIndex等框架
- 有LLM API调用经验
- 了解向量数据库优先
加分项：
- 有多智能体系统经验
- 熟悉FastAPI
- 有实际AI项目经验
"""

resume = """
教育背景：XX大学硕士，研究方向：多智能体路径规划
技术栈：Python、DeepSeek API、RAG系统开发、Agent开发
项目经历：
- 简历优化助手：基于LLM和System Prompt开发，支持多轮对话
- 企业知识库问答系统：基于RAG架构，实现文档智能问答
- 代码审查Agent：实现工具调用和自动化代码分析
- AI求职助手：多Agent协作系统，三个Agent分工完成求职分析
研究经历：多智能体路径规划，发表论文XX篇
"""

run_job_agent(jd, resume)