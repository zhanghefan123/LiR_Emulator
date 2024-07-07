import os
import functools


class EnvLoader:
    def __init__(self):
        self.frr_enabled = os.getenv("FRR_ENABLED")
        self.lir_enabled = os.getenv("LIR_ENABLED")
        self.container_name = os.getenv("CONTAINER_NAME")
        self.node_type = os.getenv("NODE_TYPE")
        self.node_id = os.getenv("NODE_ID")
        self.default_bloom_filter_length = os.getenv("DEFAULT_BLOOM_FILTER_LENGTH")
        self.default_hash_seed = os.getenv("DEFAULT_HASH_SEED")
        self.default_number_of_hash_funcs = os.getenv("DEFAULT_NUMBER_OF_HASH_FUNCS")
        self.encoding_count = os.getenv("ENCODING_COUNT")
        self.validation_method = os.getenv("VALIDATION_METHOD")
        self.has_validation_method_or_not = self.has_validation_method()
        print(self, flush=True)

    def has_validation_method(self):
        """
        判断是否有 validation method
        :return:
        """
        if self.validation_method in ["ICING", "OPT", "BPT"]:
            return True
        else:
            return False

    def __str__(self):
        """
        返回环境变量的列表
        """
        str_list = [f"{key}->{self.__dict__[key]}" for key in self.__dict__.keys()]
        return functools.reduce(lambda str1, str2: f"{str1}\n{str2}", str_list)
