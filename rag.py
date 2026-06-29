from openai import OpenAI

client = OpenAI(
    api_key="sk-6df1af5b69874d3a82651eacee3af239",
    base_url="https://api.deepseek.com"
)

# 读取文档并切块
with open("company.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]

print("文档加载完成，可以开始提问了\n")

def find_relevant(query, chunks):
    # 让AI找出最相关的段落
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "从以下段落中找出和问题最相关的1-2段，只返回段落原文，不要加任何解释。\n\n段落：\n" + "\n---\n".join(chunks)},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content

while True:
    query = input("你：")
    context = find_relevant(query, chunks)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": f"你是公司助手，只根据以下资料回答问题，资料之外的内容说不知道：\n\n{context}"},
            {"role": "user", "content": query}
        ]
    )

    reply = response.choices[0].message.content
    print(f"\nAI：{reply}\n")