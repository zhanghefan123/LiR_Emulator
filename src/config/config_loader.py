import functools

if __name__ == "__main__":
    import sys
    sys.path.append("../../")
import yaml
from src.tools.network import ip_getter as igm


class ConfigLoader:
    def __init__(self):
        self.integer_vars = ["num_of_orbit", "sat_per_orbit", "default_bloom_filter_length",
                             "default_hash_seed", "default_number_of_hash_funcs", "listening_port"]
        # ------------------ 卫星相关参数 ------------------
        self.satellite_image_name = None # 卫星镜像名称
        self.num_of_orbit = None  # 轨道数量
        self.sat_per_orbit = None  # 每轨道卫星数量
        # ------------------ 卫星相关参数 ------------------
        # ------------------------- 网络相关参数 -------------------------
        self.local_ip_address = igm.IpGetter.get_host_ip()  # 本地 ip 地址
        self.docker_request_url = f"http://{self.local_ip_address}:2375"  # docker 请求地址
        self.listening_port = None
        # ------------------------- 网络相关参数 -------------------------
        # ------------------------ 布隆过滤器参数 ------------------------
        self.default_bloom_filter_length = None  # 默认的布隆过滤器长度(bit)
        self.default_hash_seed = None  # 默认的哈希种子
        self.default_number_of_hash_funcs = None  # 默认的哈希函数个数
        # ------------------------ 布隆过滤器参数 ------------------------
        # ------------------------ 地址相关参数 --------------------------
        self.abs_dir_of_projects = None
        self.relative_dir_of_frr = None
        self.relative_dir_of_lir_identifiers = None
        self.relative_dir_of_lir_routes = None
        self.relative_dir_of_id_to_ip_mapping = None
        self.relative_dir_of_images_manager = None
        # ------------------------ 地址相关参数 --------------------------
        # ------------------------ 功能模块参数 --------------------------
        self.frr_enabled = None
        self.lir_enabled = None
        # ------------------------ 功能模块参数 --------------------------

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, item):
        """
        使得对象变得 subscriptable 可索引的, 即 object[xxx]
        :param item: 传入的键
        :return:
        """
        if item not in self.__dict__.keys():
            raise ValueError("config loader does not contain this property!")
        return self.__dict__[item]

    def __setitem__(self, key, value):
        """
        使得可以利用键值对进行设置，即 object[key]=value
        :param key:
        :param value:
        :return:
        """
        if key not in self.__dict__.keys():
            raise ValueError("config loader does not contain this property!")
        self.__dict__[key] = value

    def load(self, configuration_file_path: str = "../../resources/config.yaml",
             selected_config: str = "lir"):
        """
        进行配置的加载
        :param configuration_file_path: 配置文件的路径 (与 sys.path 无关, 搜索模块才会看 sys.path)
        :param selected_config: 选择的配置
        :return:
        """
        with open(file=configuration_file_path, mode='r', encoding="utf-8") as f:
            selected_config_data = yaml.load(stream=f, Loader=yaml.FullLoader).get(selected_config, None)
        if selected_config_data is None:
            raise RuntimeError("cannot find specified yaml config!")
        else:
            for config_loader_prop in self.__dict__.keys():
                yaml_result = selected_config_data.get(config_loader_prop, None)
                if yaml_result is None:
                    pass
                else:
                    if config_loader_prop in self.integer_vars:
                        self[config_loader_prop] = int(yaml_result)
                    else:
                        self[config_loader_prop] = yaml_result
        self.check()

    def check(self):
        """
        检查是否所有元素都是非空的
        :return:
        """
        if not all([str(self.__dict__[item]) for item in self.__dict__.keys()]):
            raise ValueError("not all properties are initialized!")

    def __str__(self) -> str:
        """
        :return: 加载进对象的配置
        """
        str_list = [f"{item}->{self.__dict__[item]}" for item in self.__dict__.keys()]
        return functools.reduce(lambda str1, str2: f"{str1}\n{str2}", str_list)


if __name__ == "__main__":
    config_loader = ConfigLoader()
    config_loader.load()
    print(config_loader)
