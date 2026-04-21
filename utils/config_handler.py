"""
yaml 格式 像是字典类的 来管理配置项
k: v
"""
import yaml
from utils.path_tool import get_abs_path

# 加载和RAG的相关配置文件
def load_rag_config(config_path: str=get_abs_path("config/rag.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:  # r读取形式
        return yaml.load(f, Loader=yaml.FullLoader)   #把整个配置文件 加载出来 返回出来

# 加载和向量数据库的相关配置文件
def load_chroma_config(config_path: str=get_abs_path("config/chroma.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

# 加载和提示词的相关配置文件
def load_prompts_config(config_path: str=get_abs_path("config/prompts.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

# 加载和agent的相关配置文件
def load_agent_config(config_path: str=get_abs_path("config/agent.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

# 四个变量 保存了 这四个函数的返回值 也就是 四个配置文件 后续的话 可以直接引用这四个变量了
rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
agent_conf = load_agent_config()


if __name__ == '__main__':
    print(rag_conf["chat_model_name"])
