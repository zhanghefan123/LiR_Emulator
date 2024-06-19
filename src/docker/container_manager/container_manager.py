from typing import Mapping
from src.docker.container_manager.impl import aiohttp_invoker as aim


class ContainerManager:
    def __init__(self, docker_request_url: str):
        """
        初始化容器管理器
        :param docker_request_url: docker daemon 监听的地址
        """
        self.aiohttp_invoker = aim.AioHttpInvoker(url=docker_request_url)

    async def create_container(self, image_name: str, container_name: str,
                               container_index: int, environment: list = None,
                               volumes: list = None, exposed_ports: Mapping = None,
                               port_bindings: Mapping = None, command: str = None,
                               working_dir: str = None, cpu_limit: int = None,
                               memory_limit: int = None) -> (int, str):
        """
        进行容器的创建
        :param image_name: 镜像的名称
        :param container_name: 容器的名称
        :param container_index: 容器的索引
        :param environment: 环境变量
        :param volumes: 容器数据卷
        :param exposed_ports: 暴露的端口
        :param port_bindings: 端口映射
        :param command: 执行的命令
        :param working_dir: 工作目录
        :param cpu_limit: cpu 限制
        :param memory_limit: 内存限制
        :return: 传入的容器的索引, 创建出来的容器的 ID
        """

        url_parameters = {
            "name": container_name,
        }
        hostConfig = {
            "CapAdd": ["NET_ADMIN"],
            "Privileged": True
        }
        if cpu_limit:
            hostConfig["NanoCpus"] = cpu_limit
        if memory_limit:
            hostConfig["Memory"] = memory_limit
        body_parameters = {
            "Image": image_name,
            "Detach": True,
            "HostConfig": hostConfig
        }
        if environment is not None:
            body_parameters["Env"] = environment
        if volumes is not None:
            body_parameters["HostConfig"]["Binds"] = volumes
        if exposed_ports is not None:
            body_parameters["ExposedPorts"] = exposed_ports
        if port_bindings is not None:
            body_parameters["HostConfig"]["PortBindings"] = port_bindings
        if command is not None:
            body_parameters["Cmd"] = command
        if working_dir is not None:
            body_parameters["WorkingDir"] = working_dir
        container_id = await self.aiohttp_invoker.create_container(url_parameters=url_parameters,
                                                                   body_parameters=body_parameters)
        return container_index, container_id

    async def start_container(self, container_id: str):
        """
        根据容器id进行容器的启动
        :param container_id:
        """
        await self.aiohttp_invoker.start_container(container_id=container_id)

    async def stop_container(self, container_id: str):
        """
        根据容器id进行容器的停止
        :param container_id: 容器的id
        """
        await self.aiohttp_invoker.stop_container(container_id)

    async def delete_container(self, container_id: str):
        """
        根据容器id进行容器的删除
        :param container_id: 容器的id
        """
        await self.aiohttp_invoker.delete_container(container_id)

    async def inspect_container(self, container_id: str):
        """
        根据容器id进行容器的检查
        :param container_id: 容器的id
        :return: 返回的是容器的相关信息
        """
        response = await self.aiohttp_invoker.inspect_container(container_id)
        return response

    async def inspect_all_containers(self):
        """
        将系统之中现有的容器全部搜索到
        :return: 返回的是所有容器的相关信息
        """
        response = await self.aiohttp_invoker.inspect_all_containers()
        return response
