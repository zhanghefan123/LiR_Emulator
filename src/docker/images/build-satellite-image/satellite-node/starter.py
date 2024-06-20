import signal
import time
from loguru import logger


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
            self.never_stop_until_sigterm()
        except Exception as e:
            self.logger.error(e)


if __name__ == "__main__":
    starter = Starter()
    starter.main_logic()
