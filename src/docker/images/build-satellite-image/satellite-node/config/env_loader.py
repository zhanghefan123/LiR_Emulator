import os
import functools


class EnvLoader:
    def __init__(self):
        self.frr_enabled = os.getenv("FRR_ENABLED")
        self.lir_enabled = os.getenv("LIR_ENABLED")
        self.container_name = os.getenv("CONTAINER_NAME")
        self.node_type = os.getenv("NODE_TYPE")
        self.node_id = os.getenv("NODE_ID")
        print(self, flush=True)

    def __str__(self):
        """
        返回环境变量的列表
        """
        str_list = [f"{key}->{self.__dict__[key]}" for key in self.__dict__.keys()]
        return functools.reduce(lambda str1, str2: f"{str1}\n{str2}", str_list)
