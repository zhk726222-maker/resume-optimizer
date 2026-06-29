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

注意：
- 语气专业但友好
- 修改建议要具体，不要泛泛而谈
- 如果用户没发简历就问其他问题，提醒他先粘贴简历内容
"""

history = [
    {"role": "system", "content": system_prompt}
]

print("=== 简历优化助手 ===")
print("请把你的简历内容粘贴进来，我来帮你优化\n")

while True:
    user_input = input("你：")
    history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=history
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})

    print(f"\n顾问：{reply}\n")