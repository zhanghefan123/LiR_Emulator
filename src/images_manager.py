if __name__ == "__main__":
    import sys

    sys.path.append("../")

from PyInquirer import prompt
from src.tools.directory import work_dir_changer as wdcm
from src.config import config_loader as clm
import os

POSSIBLE_IMAGES = [
    "ubuntu-modified",
    "ubuntu-python",
    "satellite"
]

QUESTION_FOR_IMAGE = [
    {
        "type": "list",
        "name": "image",
        "message": "请选择需要操作的镜像:",
        "choices": POSSIBLE_IMAGES
    }
]

POSSIBLE_OPTIONS = [
    "build",
    "remove",
    "rebuild"
]

QUESTION_FOR_OPTION = [
    {
        "type": "list",
        "name": "option",
        "message": "请选择进行的操作:",
        "choices": POSSIBLE_OPTIONS
    }
]


class ImagesManager:
    def __init__(self, config_loader: clm.ConfigLoader):
        self.path_of_images_manager = f"{config_loader.abs_dir_of_projects}/{config_loader.relative_dir_of_images_manager}"
        self.user_select_image = None
        self.user_select_option = None

    def get_user_input(self):
        """
        获取用户选择的镜像，以及进行的操作
        :return:
        """
        self.user_select_image = prompt(QUESTION_FOR_IMAGE)["image"]
        self.user_select_option = prompt(QUESTION_FOR_OPTION)["option"]

    def start(self):
        """
        开始进行调用
        """
        self.get_user_input()
        with wdcm.WorkDirChanger(destination_dir=self.path_of_images_manager):
            os.system(f"./images_manager -i {self.user_select_image} -o {self.user_select_option}")


if __name__ == "__main__":
    config_loader_tmp = clm.ConfigLoader()
    config_loader_tmp.load(configuration_file_path="../resources/config.yaml")
    images_manager = ImagesManager(config_loader=config_loader_tmp)
    images_manager.start()
