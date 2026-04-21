from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from utils.config_handler import rag_conf


"""
用“工厂模式”统一创建两种模型：聊天模型（LLM）和向量模型（Embedding）

据配置 rag_conf，创建
一个聊天模型 chat_model
一个向量模型 embed_model
并且用“工厂类”把创建逻辑统一封装起来。

BaseModelFactory        # 抽象父类（规范）
├── ChatModelFactory    # 子类：创建聊天模型
└── EmbeddingsFactory   # 子类：创建向量模型

chat_model = ...
embed_model = ...
"""
#所有子类必须实现 generator() 方法
class BaseModelFactory(ABC):            #
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]: ##所有子类必须实现 generator() 方法
        pass

#
class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]: # 创建聊天模型
        return ChatTongyi(model=rag_conf["chat_model_name"],dashscope_api_key="你的apikey")   #等价于  ChatTongyi(model="qwen3-max")


class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]: #创建 embedding 模型
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"],dashscope_api_key="你的apikey")  # 等价于 DashScopeEmbeddings(model="text-embedding-v1")


chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()
#👉 做了两件事：

#创建工厂对象
#调用 generator() 生成模型

"""
核心原因：可扩展性

未来你可能：

想换模型（OpenAI / Claude / 本地模型）
想做 A/B 测试
想根据配置动态切换模型

这段代码用“工厂模式”统一创建聊天模型和向量模型，让模型切换、扩展、维护更方便，是一个典型的 RAG 工程结构写法
"""