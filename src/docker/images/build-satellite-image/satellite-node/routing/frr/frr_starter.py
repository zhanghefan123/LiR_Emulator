import os
from config import env_loader as elm


class FrrStarter:
    def __init__(self, env_loader: elm.EnvLoader):
        """
        进行 frr 启动器的初始化
        :param env_loader: 环境变量管理器
        """
        self.frr_enabled = env_loader.frr_enabled
        self.node_type = env_loader.node_type
        self.node_id = env_loader.node_id
        self.container_name = env_loader.container_name
        self.frr_configuration_file = f"/configuration/frr/{self.container_name}.conf"

    def start_frr(self):
        """
        拷贝配置文件, 启动frr
        """
        if self.frr_enabled:
            copy_frr_config_command = f"cp {self.frr_configuration_file} /etc/frr/frr.conf"
            start_frr_command = f"service frr start"
            os.system(copy_frr_config_command)
            os.system(start_frr_command)
