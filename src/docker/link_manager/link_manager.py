from typing import List
from src.entities import link as lm
from src.tools.concurrency import multithread_executor as mem


class LinkManager:
    def __init__(self, links: List[lm.Link]):
        """
        链路生成器
        :param links: 所有的链路
        """
        self.links = links
        self.multithread_executor = mem.MultiThreadExecutor(max_workers=60)

    def generate_links(self):
        """
        生成所有的链路
        """
        tasks = []
        args = []
        for link in self.links:
            tasks.append(link.generate_single_actual_link)
            args.append(())
        self.multithread_executor.start(task_list=tasks, args_list=args, description="create links process")
