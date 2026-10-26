# -*-coding:utf-8 -*- #
# ---------------------------------------------------------------------------
# ProjectName:   11_company_project
# FileName:      llm.py
# Author:       wyh
# ---------------------------------------------------------------------------
# 把本地运行的qwen2.5:3b-instruct 封装成项目随时可调用的工具
# 导包
import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

# 加载.env
load_dotenv()

# 定义获取本地大模型的函数
def get_llm(temperature: float = 0.1):
    """
    封装本地 Ollama 大模型
    使用 qwen2.5:3b-instruct，温度调低(0.1)以保证输出的稳定性和准确性
    """
    # 创建一个本地大模型
    '''    
    llm = ChatOllama(
        # 指定模型名称
        model="qwen2.5:3b-instruct",
        # 指定温度参数
        temperature=temperature,
        # 指定基础URL
        base_url="http://localhost:11434",
    )
    '''
    llm = ChatDeepSeek(
        model = 'deepseek-chat', # deepseek-reasoner
        temperature=0.1,
        max_tokens=1024,
        max_retries=2,
    )
    return llm

# 定义与本地大模型进行对话的函数
def chat_with_llm(system_prompt: str, user_prompt: str) -> str:
    """
    快速调用本地大模型（用于后续调试）
    """
    # 创建一个本地大模型实例
    llm = get_llm()
    # 创建一个消息列表，包含系统提示和用户提示
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]
    # 调用大模型并获取响应
    response = llm.invoke(messages)
    # 返回大模型的响应内容
    return response.content