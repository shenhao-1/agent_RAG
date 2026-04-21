import os
import hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader


def get_file_md5_hex(filepath: str):                    # 获取文件的md5的十六进制字符串

    if not os.path.exists(filepath):                    # 不存在
        logger.error(f"[md5计算]文件{filepath}不存在")
        return

    if not os.path.isfile(filepath):                    #路径不对
        logger.error(f"[md5计算]路径{filepath}不是文件")
        return

    md5_obj = hashlib.md5()                             #hashlib 得到  md5的 对象

    chunk_size = 4096       # 4KB分片，避免文件过大爆内存     # 避免过大 一批一批去更新md5 不然效率太低
    try:
        with open(filepath, "rb") as f:                 # 必须二进制读取 rb 是二进制读取
            while chunk := f.read(chunk_size):          #: =  是 chunk =
                md5_obj.update(chunk)                   # 更新一下md5 对象

            """
            ：= 
            chunk = f.read(chunk_size)
            while chunk:
                
                md5_obj.update(chunk)
                chunk = f.read(chunk_size)
            """   # 这时候 全部跑完了 md5——obj 包含了整个文件
            md5_hex = md5_obj.hexdigest()               #  计算md5值
            return md5_hex
    except Exception as e:
        logger.error(f"计算文件{filepath}md5失败，{str(e)}")
        return None

                            # 路径     允许的文件类型
def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):        # 返回文件夹内的文件列表（允许的文件后缀） 比如我只要pdf文件 或者是txt文件
    files = []

    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹")
        return allowed_types

    for f in os.listdir(path):            # 列出所有文件对象
        if f.endswith(allowed_types):       # f的文件在这个允许的文件里面
            files.append(os.path.join(path, f))              # 拿到这个文件的全路径

    return tuple(files)                                             # 返回出去（元组类型 不允许改变了）


def pdf_loader(filepath: str, passwd=None) -> list[Document]:  # pdf 加载   参数（路径 密码） 返回一个列表 里面都是 document对象
    return PyPDFLoader(filepath, passwd).load()


def txt_loader(filepath: str) -> list[Document]:                # txt加载
    return TextLoader(filepath, encoding="utf-8").load()
