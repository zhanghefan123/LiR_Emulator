
class IdToIpMappingLoader:
    def __init__(self, id_to_ip_mapping_file_path: str = "/configuration/network/address_mapping.conf"):
        """
        ip 地址映射加载器的初始化
        """
        self.id_to_ip_mapping_file_path = id_to_ip_mapping_file_path

    def load(self):
        """
        进行 id 到 ip 的映射的加载
        :return:
        """
        delimiter = "|"
        id_to_ip_mapping = {}
        with open(self.id_to_ip_mapping_file_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                # satellite1|192.168.0.34/30|192.168.0.37/30
                items = line.split(delimiter)
                id_to_ip_mapping[items[0]] = [item[:-3] for item in items[1:]]
        return id_to_ip_mapping


