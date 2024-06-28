from pyroute2.netlink import NLM_F_REQUEST, genlmsg
from pyroute2.netlink.generic import GenericNetlinkSocket
from PyInquirer import prompt
from loguru import logger

if __name__ == "__main__":
    import sys

    sys.path.append("../../")

QUESTIONS_FOR_NETLINK_COMMAND = [
    {
        "type": "list",
        "name": "command",
        "message": "Please select the command: ",
        "choices": ["insert route", "calculate length", "search route", "find net interface",
                    "retrieve interface table", "get bind id", "exit"]
    }
]
QUESTIONS_FOR_SOURCE_AND_DEST = [
    {
        "type": "input",
        "name": "source",
        "message": "Please input the source id: "
    },
    {
        "type": "input",
        "name": "destination",
        "message": "Please input the destination id: "
    }
]
QUESTIONS_FOR_CMD_CALCULATE_LENGTH = [
    {
        "type": "input",
        "name": "message",
        "message": "Please input the message you want to calculate: "
    }
]
QUESTIONS_FOR_CMD_FIND_DEV_BY_INDEX = [
    {
        "type": "input",
        "name": "interface",
        "message": "Please input the ifindex of the network interface: "
    }
]

CMD_UNSPEC = 0
CMD_REQ = 1


class NetlinkMessageType:
    CMD_EXIT = -1  # 退出命令
    CMD_UNSPEC = 0
    CMD_INSERT_ROUTES = 1  # 进行路由的插入
    CMD_CALCULATE_LENGTH = 2  # 进行长度的计算
    CMD_SEARCH_ROUTES = 3  # 进行路由条目的搜索
    CMD_FIND_DEV_BY_INDEX = 4  # 通过 ifindex 进行接口的名称的查找
    CMD_BIND_NET_TO_SAT_NAME = 5  # 将网络命名空间和卫星名称进行绑定
    CMD_SET_BLOOM_FILTER_ATTRS = 6  # 设置布隆过滤器的属性
    CMD_CONSTRUCT_NEW_INTERFACE_TABLE = 7  # 进行新的接口表的创建
    CMD_RETRIEVE_NEW_INTERFACE_TABLE = 8  # 进行接口表的返回
    CMD_GET_BIND_ID = 9  # 进行绑定的节点 ID 的查找
    CMD_SET_ENCODING_COUNT = 10


# 消息的组成
class NetlinkMessageFormat(genlmsg):
    nla_map = (
        ('RLINK_ATTR_UNSPEC', 'none'),
        ('RLINK_ATTR_DATA', 'asciiz'),
        ('RLINK_ATTR_LEN', 'uint32'),
    )


class NetlinkClient(GenericNetlinkSocket):
    def __init__(self):
        super().__init__()
        self.logger = logger
        self.bind("EXMPL_GENL", NetlinkMessageFormat)

    @classmethod
    def get_selected_command(cls):
        """
        进行命令用户命令的获取
        :return: 返回用户选择的命令类型 类型一般为 (NetlinkMessageType)
        """
        selected_command_answer = prompt(QUESTIONS_FOR_NETLINK_COMMAND)["command"]
        if selected_command_answer == "insert route":
            selected_command = NetlinkMessageType.CMD_INSERT_ROUTES
        elif selected_command_answer == "calculate length":
            selected_command = NetlinkMessageType.CMD_CALCULATE_LENGTH
        elif selected_command_answer == "search route":
            selected_command = NetlinkMessageType.CMD_SEARCH_ROUTES
        elif selected_command_answer == "find net interface":
            selected_command = NetlinkMessageType.CMD_FIND_DEV_BY_INDEX
        elif selected_command_answer == "retrieve interface table":
            selected_command = NetlinkMessageType.CMD_RETRIEVE_NEW_INTERFACE_TABLE
        elif selected_command_answer == "get bind id":
            selected_command = NetlinkMessageType.CMD_GET_BIND_ID
        elif selected_command_answer == "exit":
            selected_command = NetlinkMessageType.CMD_EXIT
        else:
            raise ValueError("unsupported command")
        return selected_command

    def send_netlink_data(self, data: str, message_type: int):
        """
        发送 netlink 数据
        :param data: 数据
        :param message_type: 消息类型
        :return:
        """
        self.logger.success("---------SEND KERNEL REQUEST----------")
        msg = NetlinkMessageFormat()
        msg["cmd"] = message_type
        msg["version"] = 1
        msg["attrs"] = [("RLINK_ATTR_DATA", data)]
        kernel_response = self.nlm_request(msg, self.prid, msg_flags=NLM_F_REQUEST)
        self.logger.success("---------SEND KERNEL REQUEST----------")
        self.logger.success("-------RECEIVE KERNEL RESPONSE--------")
        data_part = kernel_response[0]
        self.logger.info(data_part.get_attr('RLINK_ATTR_LEN'))
        self.logger.info(data_part.get_attr('RLINK_ATTR_DATA'))
        self.logger.success("-------RECEIVE KERNEL RESPONSE--------")

    def handle_different_command(self, command):
        """
        进行各种命令的处理
        :param command: 用户选择的命令
        :return 返回出错的原因
        """
        if command == NetlinkMessageType.CMD_INSERT_ROUTES:
            self.logger.error("插入路由命令未实现")
        elif command == NetlinkMessageType.CMD_CALCULATE_LENGTH:
            user_message = prompt(QUESTIONS_FOR_CMD_CALCULATE_LENGTH)["message"]  # 让用户输入消息
            self.send_netlink_data(user_message, message_type=command)
        elif command == NetlinkMessageType.CMD_SEARCH_ROUTES:
            source_and_dest = prompt(QUESTIONS_FOR_SOURCE_AND_DEST)
            source = int(source_and_dest["source"])
            destination = int(source_and_dest["destination"])
            self.send_netlink_data(f"{source},{destination}", message_type=command)
        elif command == NetlinkMessageType.CMD_FIND_DEV_BY_INDEX:
            interface = prompt(QUESTIONS_FOR_CMD_FIND_DEV_BY_INDEX)["interface"]
            self.send_netlink_data(f"{interface}", message_type=command)
        elif command == NetlinkMessageType.CMD_RETRIEVE_NEW_INTERFACE_TABLE:
            self.send_netlink_data("", message_type=command)
        elif command == NetlinkMessageType.CMD_GET_BIND_ID:
            self.send_netlink_data("", message_type=command)


if __name__ == "__main__":
    netlink_client = NetlinkClient()
    while True:
        user_selected_command = NetlinkClient.get_selected_command()
        if user_selected_command == NetlinkMessageType.CMD_EXIT:
            break
        else:
            netlink_client.handle_different_command(command=user_selected_command)
    netlink_client.logger.success("退出了 Netlink 客户端")

