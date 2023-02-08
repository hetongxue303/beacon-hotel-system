import os


def create_dir(file_name: str) -> str:
    """
    创建文件夹
    :param file_name: 文件名
    :return:
    """
    current_path = os.path.dirname(__file__)  # 获取当前文件夹

    parent_path = os.path.abspath(os.path.join(current_path, ".."))  # 获取当前文件夹的上一层文件

    path = parent_path + os.sep + file_name + os.sep  # 拼接日志文件夹的路径

    os.makedirs(path, exist_ok=True)  # 如果文件夹不存在就创建

    return path
