import os


class WorkDirChanger:
    def __init__(self, destination_dir: str):
        """
        :param destination_dir: 要切换到的工作目录
        """
        self.destination_dir = destination_dir
        self.original_dir = os.getcwd()

    def __enter__(self):
        """
        切换到指定的工作目录
        """
        os.chdir(self.destination_dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        还原到原工作目录
        """
        os.chdir(self.original_dir)
