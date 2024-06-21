import signal
import time
import traceback
from loguru import logger
from routing import frr_starter as fmm
from config import env_loader as elm


def signal_sigterm_decorator(func):
    """
    信号装饰器，让传入的函数能够响应 linux 内核信号
    :param func: 传入的函数
    :return: 装饰的函数
    """

    def signal_decorated(*args, **kwargs):
        signal.signal(signal.SIGTERM, lambda: exit())  # 不用管这个报错
        func(*args, **kwargs)

    return signal_decorated


class Starter:
    def __init__(self):
        self.logger = logger
        self.env_loader = elm.EnvLoader()
        self.frr_starter = fmm.FrrStarter(env_loader=self.env_loader)

    @signal_sigterm_decorator
    def never_stop_until_sigterm(self):
        """
        只有收到了 SIGTERM 的时候才会退出
        :return:
        """
        while True:
            time.sleep(1)

    def main_logic(self):
        try:
            self.frr_starter.start_frr()
            self.never_stop_until_sigterm()
        except Exception:
            self.logger.error(traceback.format_exc())


if __name__ == "__main__":
    starter = Starter()
    starter.main_logic()
