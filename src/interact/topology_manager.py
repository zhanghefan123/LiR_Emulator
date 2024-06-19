from PyInquirer import prompt
from src.config import config_loader as clm
from src.entities import logical_constellation as lcm
from src.docker.container_manager import container_manager as cmm
from src.routing.frr import frr_config_generator as fcgm
from src.routing.lir import lir_config_generator as lcgm
from src.routing.lir import lir_route_calculator as lrcm
from enum import Enum
import loguru

POSSIBLE_COMMANDS = [
    "create",
    "start",
    "destroy"
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

    def __init__(self, config_loader: clm.ConfigLoader, logger: loguru.Logger):
        """
        :param config_loader: 配置加载对象
        :param logger: 日志记录器
        """
        self.config_loader = config_loader
        self.topology_state = TopologyManager.TopologyState.NOT_CREATED
        self.logger = logger
        self.logical_constellation = lcm.LogicalConstellation(config_loader=config_loader)
        self.container_manager = cmm.ContainerManager(docker_request_url=config_loader.docker_request_url)
        self.frr_config_generator = fcgm.FrrConfigGenerator(satellites=self.logical_constellation.satellites,
                                                            generate_destination=f"{self.config_loader.abs_dir_of_projects}/{self.config_loader.relative_dir_of_frr}")
        self.lir_identifiers_generator = lcgm.LirConfigGenerator(satellites=self.logical_constellation.satellites,
                                                                 generate_destination=f"{self.config_loader.abs_dir_of_projects}/{self.config_loader.relative_dir_of_lir_identifiers}")
        self.lir_routes_generator = lrcm.LirRouteCalculator(satellites=self.logical_constellation.satellites,
                                                            lir_link_identifiers=self.logical_constellation.lir_link_identifiers,
                                                            map_from_source_dest_pair_to_lir_link_identifier=self.logical_constellation.map_from_source_dest_pair_to_lir_link_identifier,
                                                            generate_destination=f"{self.config_loader.abs_dir_of_projects}/{self.config_loader.relative_dir_of_lir_routes}")

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
            if command == "create":
                pass
            elif command == "start":
                reason = "topology not created"
            elif command == "destroy":
                reason = "topology not created"
        elif self.topology_state == TopologyManager.TopologyState.CREATED:
            if (command == "start") or (command == "destroy"):
                pass
            elif command == "created":
                reason = "topology already created"
        elif self.topology_state == TopologyManager.TopologyState.STARTED:
            if command == "destroy":
                pass
            elif command == "create":
                reason = "topology already started"
            elif command == "start":
                reason = "topology already started"
            else:
                result = False
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
        selected_command = prompt(QUESTION_FOR_COMMAND)
        valid, reason = self.validate_command(selected_command)
        if not valid:
            self.logger.error(reason)
        else:
            # --------------------------------------------------
            try:
                if selected_command == "create":
                    self.create_topology()
                elif selected_command == "start":
                    pass
                elif selected_command == "destroy":
                    pass
                self.change_state(command=selected_command)
            except Exception as e:
                self.logger.error(e)

    def generate_config_files(self):
        """
        进行配置文件的初始化
        """
        self.frr_config_generator.generate()
        self.lir_identifiers_generator.generate()

    def create_topology(self):
        """
        调用 container_manager 进行拓扑的创建
        :return:
        """
        self.generate_config_files()
