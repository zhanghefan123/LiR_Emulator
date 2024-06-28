from PyInquirer import prompt
from routing.lir.apps.udp.udp_client import udp_client as ucm
from routing.lir.apps.udp.udp_server import udp_server as usm
from routing.lir.tables import routes_loader as rlm

QUESTION_FOR_PROTOCOL = [
    {
        "type": "list",
        "name": "app",
        "message": "请选择要启动的应用: ",
        "choices": ["client", "server"]
    }
]


class AppManager:
    def __init__(self):
        self.selected_app = None
        self.routes_loader = rlm.RoutesLoader()

    def get_user_input(self):
        self.selected_app = prompt(QUESTION_FOR_PROTOCOL)["app"]

    def handle_different_app(self):
        if self.selected_app == "client":
            udp_client = ucm.UdpClient(routes_loader=self.routes_loader)
            udp_client.start()
        elif self.selected_app == "server":
            udp_server = usm.UdpServer()
            udp_server.start()
        else:
            raise ValueError("不支持的应用")

    def start(self):
        self.get_user_input()
        self.handle_different_app()


if __name__ == "__main__":
    app_manager = AppManager()
    app_manager.start()
