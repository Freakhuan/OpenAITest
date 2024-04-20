import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# 加载.env 到环境变量
load_dotenv(find_dotenv())

# 配置 OpenAI 服务

client = OpenAI()
prompt = """
你的工作：你是一名上海的导游，负责接待游客。
输出格式：直接回答问题，不要输出其他内容。
回答不要出现"Assistant："
"""

# 基于 prompt 生成文本
# 默认使用 gpt-3.5-turbo 模型
def get_completion(prompt, response_format="text", model=os.getenv('MY_MODEL')):
    messages = [{"role": "user", "content": prompt}]    # 将 prompt 作为用户输入
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,                                  # 模型输出的随机性，0 表示随机性最小
        # 返回消息的格式，text 或 json_object
        response_format={"type": response_format},
    )
    return response.choices[0].message.content          # 返回模型生成的文本


if __name__ == '__main__':
    # 交互模式 “提问：”，输入后回车
    # 退出模式 “退出”，输入后回车
    # 调用get_completion 实现多轮对话
    while True:
        text = input("提问：")
        if text == "退出":
            break
        prompt = prompt+"User:"+text
        response = get_completion(prompt)
        print("回答：", response)
        prompt = prompt+"\n" + "Assistant：" + response + "\n"
        # print(prompt)