import os
import tqdm


class DockerNamespaceBuilder:
    @classmethod
    def build_network_namespace(cls, pid_list: list):
        """
        利用容器的 pid 列表将容器的网络命名空间进行恢复
        :param pid_list: pid 列表
        """
        os.system(f"rm -rf /var/run/netns/*")  # 首先进行现有的网络命名空间的删除
        # 接着进行 pid 的遍历，并生成软链接
        bar_format = '{desc}{percentage:3.0f}%|{bar}|{n_fmt}/{total_fmt}'
        for pid in tqdm.tqdm(pid_list, colour="green", ncols=97, postfix="", bar_format=bar_format, desc="generate net ns process: "):
            source_file = f"/proc/{pid}/ns/net"  # 这是要用来产生软链接的源文件
            dest_file = f"/var/run/netns/{pid}"  # 这是生成的软链接
            full_command = f"ln -s {source_file} {dest_file}"
            os.system(full_command)
