import asyncio
from typing import List
from src.config import config_loader as clm
from src.docker.container_manager import container_manager as cmm
from src.entities import satellite as sm
from src.tools.progressbar import progress_bar as pbm



class SatelliteManager:
    def __init__(self, config_loader: clm.ConfigLoader):
        """
        初始化卫星管理器
        """
        self.config_loader = config_loader
        self.container_manager = cmm.ContainerManager(docker_request_url=config_loader.docker_request_url)

    async def generate_satellites(self, satellites: List[sm.Satellite]):
        """
        进行卫星节点的生成
        :param satellites 所有的卫星节点
        """
        tasks = []
        for satellite in satellites:
            # ----------------------------- 环境变量  -----------------------------
            environment = [f"SATELLITE_NAME={satellite.container_name}",
                           f"LISTENING_PORT={self.config_loader.listening_port}",
                           f"FRR_ENABLED={self.config_loader.frr_enabled}",
                           f"LIR_ENABLED={self.config_loader.lir_enabled}",
                           f"CONTAINER_NAME={satellite.container_name}",
                           f"NODE_TYPE={str(satellite.node_type)}",
                           f"NODE_ID={satellite.node_id}",
                           f"ENCODING_COUNT={self.config_loader.encoding_count}",
                           f"VALIDATION_METHOD={self.config_loader.validation_method}",
                           f"DISPLAY=unix:0.0",
                           f"GDK_SCALE",
                           f"GDK_DPI_SCALE",
                           f"DEFAULT_BLOOM_FILTER_LENGTH={self.config_loader.default_bloom_filter_length}",
                           f"DEFAULT_HASH_SEED={self.config_loader.default_hash_seed}",
                           f"DEFAULT_NUMBER_OF_HASH_FUNCS={self.config_loader.default_number_of_hash_funcs}"]
            # ----------------------------- 环境变量  -----------------------------
            # ----------------------------- 容器映射  -----------------------------
            volumes = [
                f"{self.config_loader.abs_dir_of_projects}/{self.config_loader.relative_dir_of_frr}:/configuration/frr",
                f"{self.config_loader.abs_dir_of_projects}/{self.config_loader.relative_dir_of_lir_identifiers}:/configuration/lir/identifiers",
                f"{self.config_loader.abs_dir_of_projects}/{self.config_loader.relative_dir_of_lir_routes}:/configuration/lir/routes",
                f"{self.config_loader.abs_dir_of_projects}/{self.config_loader.relative_dir_of_id_to_ip_mapping}:/configuration/network",
                f"/tmp/.X11-unix:/tmp/.X11-unix"
            ]
            # ----------------------------- 容器映射  -----------------------------
            # ----------------------------- 任务创建  -----------------------------
            task = asyncio.create_task(self.container_manager.create_container(
                image_name=self.config_loader.satellite_image_name,
                environment=environment,
                container_name=satellite.container_name,
                volumes=volumes,
                container_index=satellite.node_index
            ))
            tasks.append(task)
            # ----------------------------- 任务创建  -----------------------------
        await pbm.ProgressBar.wait_tasks_with_tqdm(tasks, description="create satellites process")
        for task in tasks:
            satellite_index, satellite_container_id = task.result()
            satellites[satellite_index].container_id = satellite_container_id

    async def start_satellites(self, satellites: List[sm.Satellite]):
        """
        进行卫星节点的启动
        :param satellites: 所有的卫星节点
        """
        tasks = []
        satellite_container_ids = [satellite.container_id for satellite in satellites]
        for container_id in satellite_container_ids:
            task = asyncio.create_task(
                self.container_manager.start_container(container_id=container_id))
            tasks.append(task)
        await pbm.ProgressBar.wait_tasks_with_tqdm(tasks, description="start satellites process")
        await self.inspect_satellites(satellites=satellites)

    async def stop_satellites(self, satellites: List[sm.Satellite]):
        """
        进行卫星的停止
        :param satellites: 所有的卫星节点
        """
        tasks = []
        satellite_container_ids = [satellite.container_id for satellite in satellites]
        for container_id in satellite_container_ids:
            task = asyncio.create_task(
                self.container_manager.stop_container(container_id))
            tasks.append(task)
        await pbm.ProgressBar.wait_tasks_with_tqdm(tasks, description="stop satellites process")

    async def remove_satellites(self, satellites: List[sm.Satellite]):
        """
        进行卫星的删除
        :param satellites: 所有的卫星节点
        """
        tasks = []
        satellite_container_ids = [satellite.container_id for satellite in satellites]
        for container_id in satellite_container_ids:
            task = asyncio.create_task(
                self.container_manager.delete_container(container_id))
            tasks.append(task)
        await pbm.ProgressBar.wait_tasks_with_tqdm(tasks, description="remove satellites process")

    async def inspect_satellites(self, satellites: List[sm.Satellite]):
        """
        进行所有卫星容器的检查, 从而获取容器的 pid 以及容器的连接网络的地址
        :param satellites: 所有的卫星节点
        """
        tasks = []
        for satellite in satellites:
            task = asyncio.create_task(self.container_manager.inspect_container(container_id=satellite.container_id,
                                                                                container_index=satellite.node_index))
            tasks.append(task)
        await pbm.ProgressBar.wait_tasks_with_tqdm(tasks, description="inspect satellites progress")
        for task in tasks:
            satellite_index, finished_task_result = task.result()
            inspect_satellite_addr = finished_task_result["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
            inspect_satellite_pid = finished_task_result["State"]["Pid"]
            satellites[satellite_index].addr_connect_to_docker_zero = inspect_satellite_addr
            satellites[satellite_index].pid = inspect_satellite_pid
