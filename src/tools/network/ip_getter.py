import socket


class IpGetter:
    @classmethod
    def get_host_ip(cls) -> str:
        """
        查询本机ip地址
        :return: ip
        """
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return ip
