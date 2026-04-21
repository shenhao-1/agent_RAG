from langchain_chroma import Chroma
from langchain_core.documents import Document
from utils.config_handler import chroma_conf
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.path_tool import get_abs_path
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger
import os


"""
向量存储的

"""
class VectorStoreService:         # 向量存储类
    def __init__(self):
        self.vector_store = Chroma(                              #  向量库
            collection_name=chroma_conf["collection_name"],        # 表名
            embedding_function=embed_model,                         # 嵌入模型
            persist_directory=chroma_conf["persist_directory"],    #路径
        )

        """
        创建一个 RecursiveCharacterTextSplitter 对象
        把它保存到当前类的 self.spliter 里
        后面你就可以用这个 spliter 去切文档
        """
        self.spliter = RecursiveCharacterTextSplitter(           # 文档分割器
            chunk_size=chroma_conf["chunk_size"],               # 分割大小
            chunk_overlap=chroma_conf["chunk_overlap"],         # 上限
            separators=chroma_conf["separators"],               # 按什么分隔符优先去切文本
            length_function=len,                                # 用什么方式计算文本长度 用长度去计算
        )

    """
    # self. vector_store 是上面的向量库  
    retriever 是检索器  as_retriever()是把“向量数据库”包装成一个“检索器对象”
     search_kwargs={"k": chroma_conf["k"]} 每次检索返回 k 条最相关的结果
     
     整体流程是 问题转向量-> 向量相似度计算->选出 Top-k ->返回这些文本   也就是 从向量数据库里生成一个检索器，每次查询时返回最相关的 k 条文本
    """

    def get_retriever(self):       # 获取检索器对象
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def load_document(self):
        """
        从数据文件夹内读取数据文件，转为向量存入向量库
        要计算文件的MD5做去重
        :return: None
        """
        # 方法内的子方法
        def check_md5_hex(md5_for_check: str):
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                # 创建文件
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()
                return False                                    # md5 没处理过

            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True     # md5 处理过

                return False            # md5 没处理过

        def save_md5_hex(md5_for_check: str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")

        def get_file_documents(read_path: str):
            if read_path.endswith("txt"):               # 如果是txt结尾的
                return txt_loader(read_path)

            if read_path.endswith("pdf"):
                return pdf_loader(read_path)

            return []           # 啥也不是就返回空
                                            # listdir_with_allowed_type list呢个方法是
        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),             # 得到绝对路径    还是呢个 get_abs方法
            tuple(chroma_conf["allow_knowledge_file_type"]),        # 变为元组  chroma_conf 是呢四个变量 是 向量库的相关配置文件
        )

        for path in allowed_files_path:
            # 获取文件的MD5
            md5_hex = get_file_md5_hex(path)       # get_file_md5 是得到md5值

            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在知识库内，跳过")
                continue

            try:    #日志打印的
                documents: list[Document] = get_file_documents(path)

                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效文本内容，跳过")
                    continue

                split_document: list[Document] = self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效文本内容，跳过")
                    continue
                # 如果上面都没有问题
                # 将内容存入向量库
                self.vector_store.add_documents(split_document)

                # 记录这个已经处理好的文件的md5，避免下次重复加载
                save_md5_hex(md5_hex)

                logger.info(f"[加载知识库]{path} 内容加载成功")
            except Exception as e:
                # exc_info为True会记录详细的报错堆栈，如果为False仅记录报错信息本身
                logger.error(f"[加载知识库]{path}加载失败：{str(e)}", exc_info=True)
                continue


if __name__ == '__main__':
    # 创建一个实例
    vs = VectorStoreService()
    # 加载知识库
    vs.load_document()
    # 拿到检索器
    retriever = vs.get_retriever()
    # 注入问题 去知识库里找相关的
    res = retriever.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("-"*20)


