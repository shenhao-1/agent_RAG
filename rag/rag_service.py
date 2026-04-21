
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model


"""
总结服务类：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
这是个工具

用户给一个问题 query，系统先去向量库里检索相关文档，再把检索到的内容拼成 context，最后连同问题一起喂给大模型生成答案
"""
def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt


class RagSummarizeService(object):

    def __init__(self):
        self.vector_store = VectorStoreService()                #向量存储 先把“知识库/向量数据库”接进来
        self.retriever = self.vector_store.get_retriever()      # 上个向量存储里面的检索器
        self.prompt_text = load_rag_prompts()                   #加载 RAG提示词 就是写的呢个 prompt_loader 读取提示词文本。
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)   # from_template 是提示词拼接
        self.model = chat_model                                 #模型  这是呢个工程模型
        self.chain = self._init_chain()                         # 用的链

        """      
            连接向量库
            拿到检索器
            读取提示词模板
            初始化大模型调用链
            根据用户问题检索资料
            把资料和问题一起发给模型
            返回最终答案
        """

    def _init_chain(self):
        chain = self.prompt_template | print_prompt | self.model | StrOutputParser()   # 提示词  打印 模型 解析器
        return chain

    def retriever_docs(self, query: str) -> list[Document]:         # 检索文档
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:                     #RAG 的总结了

        """

        :param query:
        :return:
        输入用户问题，输出最终回答
        """

        context_docs = self.retriever_docs(query)                   #先检索资料

        context = ""
        counter = 0
        for doc in context_docs:                                    #这里面是拼接字符串的
            counter += 1
            context += f"【参考资料{counter}】: 参考资料：{doc.page_content} | 参考元数据：{doc.metadata}\n"

        return self.chain.invoke(                                   #返回
            {
                "input": query,
                "context": context,
            }
        )


if __name__ == '__main__':
    rag = RagSummarizeService()

    print(rag.rag_summarize("小户型适合哪些扫地机器人"))
