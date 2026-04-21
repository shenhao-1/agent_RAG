
"""

日志工具

"""
import logging
from utils.path_tool import get_abs_path
import os
from datetime import datetime

# 日志保存的根目录
LOG_ROOT = get_abs_path("logs")

# 确保日志的目录存在
os.makedirs(LOG_ROOT, exist_ok=True)

# 日志的格式配置  error info debug
DEFAULT_LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    # 时间            名字          级别          文件名         哪一行         日志正文
)


def get_logger(
        name: str = "agent",                #日志名字
        console_level: int = logging.INFO,  #默认级别
        file_level: int = logging.DEBUG,    #文件级别
        log_file = None,                    #
) -> logging.Logger:                        # 返回一个log对象
    logger = logging.getLogger(name)        # 把名字传进去
    logger.setLevel(logging.DEBUG)          # 级别传进去

    # 避免重复添加Handler
    if logger.handlers:
        return logger

    # 控制台Handler                            # 往控制台里去写 日志
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)   # 设置 级别
    console_handler.setFormatter(DEFAULT_LOG_FORMAT) # 设置输出格式 上面配好了

    logger.addHandler(console_handler)              #

    # 文件Handler
    if not log_file:        # 日志文件的存放路径
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(file_handler)

    return logger


# 快捷获取日志器
logger = get_logger()

# 测试
if __name__ == '__main__':
    logger.info("信息日志")
    logger.error("错误日志")
    logger.warning("警告日志")
    logger.debug("调试日志")
