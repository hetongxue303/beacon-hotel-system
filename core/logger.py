import os
from loguru import logger
from utils import files

"""日志配置"""
LOGGER_DIR: str = 'logs'  # 日志文件夹名
LOGGER_NAME: str = '{time:YYYY-MM-DD_HH-mm-ss}.log'  # 日志文件名 (时间格式)
LOGGER_LEVEL: str = 'DEBUG'  # 日志等级: ['DEBUG' | 'INFO']
LOGGER_ROTATION: str = '12:00'  # 日志分片: 按 时间段/文件大小 切分日志. 例如 ["500 MB" | "12:00" | "1 week"]
LOGGER_RETENTION: str = '1 days'  # 日志保留的时间: 超出将删除最早的日志. 例如 ["1 days"]
LOGGER_ENCODING: str = 'utf-8'  # 全局编码
LOGGER_MAX: int = 3  # 最大文件数


def logger_file() -> str:
    """
    创建日志文件名
    :return: 文件名
    """

    # 创建日志文件名
    log_path: str = files.create_dir(LOGGER_DIR)

    # 创建文件列表
    file_list: list[str] = os.listdir(log_path)
    if len(file_list) > LOGGER_MAX:
        os.remove(os.path.join(log_path, file_list[0]))

    # 日志输出路径
    return os.path.join(log_path, LOGGER_NAME)


logger.add(
    logger_file(),
    encoding=LOGGER_ENCODING,
    level=LOGGER_LEVEL,
    rotation=LOGGER_ROTATION,
    retention=LOGGER_RETENTION,
    enqueue=True
)
