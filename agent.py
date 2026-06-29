from openai import OpenAI
import json

client = OpenAI(
    api_key="sk-6df1af5b69874d3a82651eacee3af239",
    base_url="https://api.deepseek.com"
)

# 定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "analyze_logic",
            "description": "分析代码的逻辑是否正确，包括算法、流程、边界条件",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "要分析的代码"}
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_bugs",
            "description": "检查代码中的潜在bug，包括语法错误、空指针、越界等",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "要检查的代码"}
                },
                "required": ["code"]
            }
        }
    }
]

# 工具的实际执行函数
def analyze_logic(code):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是代码逻辑分析专家，分析代码逻辑是否正确，给出简洁的分析报告"},
            {"role": "user", "content": f"分析这段代码的逻辑：\n{code}"}
        ]
    )
    return response.choices[0].message.content

def check_bugs(code):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是代码bug检查专家，找出代码中的潜在问题和bug"},
            {"role": "user", "content": f"检查这段代码的bug：\n{code}"}
        ]
    )
    return response.choices[0].message.content

# Agent主循环
def run_agent(user_input):
    messages = [
        {"role": "system", "content": "你是一个代码审查Agent，收到代码后必须同时调用analyze_logic和check_bugs两个工具，最后综合两个工具的结果给出完整审查报告"},
        {"role": "user", "content": user_input}
    ]

    print("\nAgent正在思考...\n")

    while True:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools
        )

        msg = response.choices[0].message

        # 如果Agent决定调用工具
        if msg.tool_calls:
            messages.append(msg)
            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                print(f">>> 正在调用工具：{name}")

                if name == "analyze_logic":
                    result = analyze_logic(args["code"])
                elif name == "check_bugs":
                    result = check_bugs(args["code"])

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        # 如果Agent给出最终回答
        else:
            print(f"审查报告：\n{msg.content}")
            break

print("=== 代码审查Agent ===")
print("请粘贴你想审查的代码\n")

while True:
    code_input = input("你：")
    run_agent(code_input)
    print()
