from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from typing import List, Tuple
import tqdm


class MultiThreadExecutor:
    def __init__(self, max_workers):
        """
        初始化多线程处理器
        :param max_workers: 最大的工作线程数量
        """
        self.max_workers = max_workers

    def start(self, task_list: List, args_list: List[Tuple], description: str, enable_tqdm: bool = True):
        """
        启动多线程执行器
        :param task_list: 任务列表
        :param args_list: 每个任务参数
        :param description: 大任务描述
        :param enable_tqdm: 是否启动 tqdm
        :return:
        """
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            all_tasks = [executor.submit(task_list[index], *(args_list[index])) for index in range(len(task_list))]
            if enable_tqdm:
                bar_format = '{desc}{percentage:3.0f}%|{bar}|{n_fmt}/{total_fmt}'
                with tqdm.tqdm(total=len(all_tasks), colour="green", ncols=97, postfix="",
                               bar_format=bar_format) as pbar:
                    pbar.set_description(description)
                    for _ in as_completed(all_tasks):
                        pbar.update(1)
            else:
                for _ in as_completed(all_tasks):
                    pass
