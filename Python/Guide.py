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
def get_completion(prompt, response_format="text", model=os.getenv('MY_MODEL')):
    """
    获取模型完成的文本。

    参数:
    - prompt: 提供给模型的提示文本，作为用户输入。
    - response_format: 希望接收的响应格式，默认为 "text"。可选值为 "text" 或 "json_object"。
    - model: 使用的模型名称，默认从环境变量 'MY_MODEL' 获取。

    返回值:
    - 模型根据 prompt 生成的文本。
    """
    # 构造用户消息
    messages = [{"role": "user", "content": prompt}]
    # 向模型发送请求，获取响应
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,  # 设置随机性为最小
        # 设置返回消息的格式
        response_format={"type": response_format},
    )
    # 从响应中提取并返回生成的文本
    return response.choices[0].message.content

if __name__ == '__main__':
    # 交互模式 “提问：”，输入后回车
    # 退出模式 “退出”，输入后回车
    # 调用get_completion 实现多轮对话
    while True:
        text = input("提问：")
        if text == "退出":
            break
        prompt = prompt+"User:"+text
        response = get_completion(prompt).replace("Assistant：", "")
        print("回答：", response)
        prompt = prompt+"\n" + "Assistant：" + response + "\n"
        # print(prompt)