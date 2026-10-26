# -*-coding:utf-8 -*- #
# ---------------------------------------------------------------------------
# ProjectName:   11_company_project
# FileName:      test_llm.py
# Author:       wyh
# ---------------------------------------------------------------------------
# # 导包
# from models.llm import chat_with_llm
#
# res = chat_with_llm(
#     system_prompt= "你是一个工业设备故障诊断助手，请用简洁的专业的中文回答。",
#     user_prompt= "电机运行时出现异常振动，可能有哪些原因？"
# )
#
# print("LLM 回复：")
# print(res)

'''
# 导包
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama

def get_llm(model_name:str = "qwen2.5:3b-instruct", temperature: float = 0.7):
    """
    封装本地Ollama大模型
    """
    llm = ChatOllama(
        model = model_name,
        temperature = temperature,
        base_url= 'http://localhost:11434'
    )
    return llm

def stream_chat_with_llm(system_prompt: str , user_prompt: str) -> str:
    """
    快速调用本地大模型
    """
    llm = get_llm()

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    # response = llm.invoke(messages)
    # return response.content

    # 流式输出
    # 使用stream返回一个生成器，遍历它
    for chunk in llm.stream(messages):
        # 实时输出内容
        print(chunk.content,end='',flush=True)
    print()

res = stream_chat_with_llm(
    system_prompt = '你是一个工业设备故障诊断助手，请用简洁的专业的中文回答。',
    user_prompt = '电机运行时出现异常振动，可能是哪些原因？'
)
# print(res) none'''