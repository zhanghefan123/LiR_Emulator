if __name__ == "__main__":
    import sys

    sys.path.append("../")
import os.path
import traceback
import asyncio
from enum import Enum
from PyInquirer import prompt
from src.docker.satellite_manager import satellite_manager as smm
from src.config import config_loader as clm
from src.entities import logical_constellation as lcm
from src.routing.frr import frr_config_generator as fcgm
from src.routing.lir import lir_config_generator as lcgm
from src.routing.lir import lir_route_calculator as lrcm
from src.network import id_to_ip_mapping_generator as itimgm

POSSIBLE_COMMANDS = [
    "create",
    "start",
    "destroy",
    "exit"
]

QUESTION_FOR_COMMAND = [
    {
        "type": "list",
        "name": "command",
        "message": "What is your command?",
        "choices": POSSIBLE_COMMANDS
    }
]


class TopologyManager:
    class TopologyState(Enum):
        NOT_CREATED = 1
        CREATED = 2
        STARTED = 3

    def __init__(self, config_loader: clm.ConfigLoader, logger):
        """
        :param config_loader: 配置加载对象
        :param logger: 日志记录器
        """
        self.config_loader = config_loader
        self.topology_state = TopologyManager.TopologyState.NOT_CREATED
        self.logger = logger
        self.logical_constellation = lcm.LogicalConstellation(config_loader=config_loader)
        self.satellite_manager = smm.SatelliteManager(config_loader=config_loader)
        self.frr_config_generator = fcgm.FrrConfigGenerator(satellites=self.logical_constellation.satellites,
                                                            generate_destination=f"{self.config_loader.abs_dir_of_projects}/{self.config_loader.relative_dir_of_frr}")
        self.lir_identifiers_generator = lcgm.LirConfigGenerator(satellites=self.logical_constellation.satellites,
                                                                 generate_destination=f"{self.config_loader.abs_dir_of_projects}/{self.config_loader.relative_dir_of_lir_identifiers}")
        self.lir_routes_generator = lrcm.LirRouteCalculator(satellites=self.logical_constellation.satellites,
                                                            lir_link_identifiers=self.logical_constellation.lir_link_identifiers,
                                                            map_from_source_dest_pair_to_lir_link_identifier=self.logical_constellation.map_from_source_dest_pair_to_lir_link_identifier,
                                                            generate_destination=f"{self.config_loader.abs_dir_of_projects}/{self.config_loader.relative_dir_of_lir_routes}")
        self.ip_to_id_mapping_generator = itimgm.IPtoIDGenerator(satellites=self.logical_constellation.satellites,
                                                                 generate_destination=f"{self.config_loader.abs_dir_of_projects}/{self.config_loader.relative_dir_of_id_to_ip_mapping}")

    def validate_command(self, command: str) -> (bool, str):
        """
        判断传入的 command 与当前的状态是否是匹配的
        :param command: 当前的命令
        :return (是否合法, 以及出错的原因)
        """
        if command not in POSSIBLE_COMMANDS:
            raise ValueError("command should be one of (create start destroy)")
        result = True
        reason = None
        if self.topology_state == TopologyManager.TopologyState.NOT_CREATED:
            if command in ["create", "exit"]:
                pass
            elif command in ["start", "destroy"]:
                result = False
                reason = "topology not created"
        elif self.topology_state == TopologyManager.TopologyState.CREATED:
            if command in ["start", "destroy"]:
                pass
            elif command in ["create", "exit"]:
                result = False
                reason = "topology already created"
        elif self.topology_state == TopologyManager.TopologyState.STARTED:
            if command == "destroy":
                pass
            elif command in ["create", "start", "exit"]:
                result = False
                reason = "topology already started"
        return result, reason

    def change_state(self, command: str):
        """
        根据命令切换到对应的状态
        :param command: 用户输入的命令
        """
        if command == "create":
            self.topology_state = TopologyManager.TopologyState.CREATED
        elif command == "start":
            self.topology_state = TopologyManager.TopologyState.STARTED
        elif command == "destroy":
            self.topology_state = TopologyManager.TopologyState.NOT_CREATED
        else:
            raise ValueError("command should be one of (create start destroy)")

    def topology_management(self):
        """
        进行拓扑的管理: 包括拓扑的创建, 启动, 销毁
        """
        # --------------------------------------------------
        while True:
            selected_command = prompt(QUESTION_FOR_COMMAND)["command"]
            valid, reason = self.validate_command(selected_command)
            if not valid:
                self.logger.error(reason)
            else:
                try:
                    if selected_command == "create":
                        self.create_topology()
                    elif selected_command == "start":
                        self.start_topology()
                    elif selected_command == "destroy":
                        if self.topology_state == TopologyManager.TopologyState.CREATED:
                            self.remove_topology()
                        elif self.topology_state == TopologyManager.TopologyState.STARTED:
                            self.stop_topology()
                            self.remove_topology()
                    elif selected_command == "exit":
                        break
                    self.change_state(command=selected_command)
                except Exception:
                    self.logger.error(traceback.format_exc())
        self.logger.success("成功退出拓扑管理程序!")

    def generate_directories(self):
        """
        进行目录的生成
        """
        dirs = [
            f"{self.config_loader.abs_dir_of_projects}/{self.config_loader.relative_dir_of_frr}",
            f"{self.config_loader.abs_dir_of_projects}/{self.config_loader.relative_dir_of_lir_identifiers}",
            f"{self.config_loader.abs_dir_of_projects}/{self.config_loader.relative_dir_of_lir_routes}",
            f"{self.config_loader.abs_dir_of_projects}/{self.config_loader.relative_dir_of_id_to_ip_mapping}"
        ]
        for directory in dirs:
            if os.path.exists(directory):
                pass
            else:
                os.system(f"mkdir -p {directory}")

    def generate_config_files(self):
        """
        进行配置文件的初始化
        """
        self.frr_config_generator.generate()
        self.lir_identifiers_generator.generate()
        self.lir_routes_generator.generate()
        self.ip_to_id_mapping_generator.generate()

    def create_topology(self):
        """
        调用 satellite_manager 进行拓扑的创建
        """
        self.generate_directories()
        self.generate_config_files()
        asyncio.run(self.satellite_manager.generate_satellites(satellites=self.logical_constellation.satellites))

    def start_topology(self):
        """
        调用 satellite_manager 进行拓扑的启动
        """
        asyncio.run(self.satellite_manager.start_satellites(satellites=self.logical_constellation.satellites))

    def stop_topology(self):
        """
        调用 satellite_manager 进行拓扑的停止
        """
        asyncio.run(self.satellite_manager.stop_satellites(satellites=self.logical_constellation.satellites))

    def remove_topology(self):
        """
        调用 satellite_manager 进行拓扑的删除
        """
        asyncio.run(self.satellite_manager.remove_satellites(satellites=self.logical_constellation.satellites))
