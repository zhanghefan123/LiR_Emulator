import scienceplots
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


class Color:
    @classmethod
    def blue(cls):
        return [57.0 / 255.0, 115.0 / 255.0, 173.0 / 255.0]

    @classmethod
    def orange(cls):
        return [240.0 / 255.0, 136.0 / 255.0, 58.0 / 255.0]

    @classmethod
    def green(cls):
        return [71.0 / 255.0, 157.0 / 255.0, 64.0 / 255.0]


class SpecificPrefix:
    @classmethod
    def get_opt_make_skb_prefix(cls):
        return "opt_make_skb_time_elapsed: "

    @classmethod
    def get_opt_forward_prefix(cls):
        return "opt_forward_time_elapsed: "

    @classmethod
    def get_icing_make_skb_prefix(cls):
        return "icing_make_skb_time_elapsed: "

    @classmethod
    def get_icing_forward_prefix(cls):
        return "icing_forward_time_elapsed: "

    @classmethod
    def get_suffix(cls):
        return "ns"


class ForwardingTimePlotterFinal:
    def __init__(self, kernel_log_file_path: str, output_figure_name: str, min_x: int, max_x: int):
        """
        进行绘图器的初始化
        :param kernel_log_file_path: 内核日志输出文件
        :param output_figure_name:  输出的图的名称
        :param min_x:  最小的x的值
        :param max_x:  最大的x的值
        """
        self.kernel_log_file_path = kernel_log_file_path
        self.output_figure_name = output_figure_name
        self.min_x = min_x
        self.max_x = max_x
        self.opt_make_skb_times = []
        self.opt_forward_skb_times = []
        self.icing_make_skb_times = []
        self.icing_forward_skb_times = []
        self.bins = np.arange(self.min_x, self.max_x, 25)

    def analyze_single_line(self, line: str):
        """
        进行某一行的分析
        :param line: 日志文件之中的某一航
        :return:
        """
        if SpecificPrefix.get_opt_make_skb_prefix() in line:
            start_index = line.find(SpecificPrefix.get_opt_make_skb_prefix()) + len(
                SpecificPrefix.get_opt_make_skb_prefix())
            end_index = line.find(SpecificPrefix.get_suffix(), start_index)
            opt_make_skb_time = float((line[start_index: end_index]).strip())
            self.opt_make_skb_times.append(opt_make_skb_time)
        elif SpecificPrefix.get_opt_forward_prefix() in line:
            start_index = (line.find(SpecificPrefix.get_opt_forward_prefix()) +
                           len(SpecificPrefix.get_opt_forward_prefix()))
            end_index = line.find(SpecificPrefix.get_suffix(), start_index)
            opt_forward_skb_time = float((line[start_index: end_index]).strip())
            self.opt_forward_skb_times.append(opt_forward_skb_time)
        elif SpecificPrefix.get_icing_make_skb_prefix() in line:
            start_index = (line.find(SpecificPrefix.get_icing_make_skb_prefix()) +
                           len(SpecificPrefix.get_icing_make_skb_prefix()))
            end_index = line.find(SpecificPrefix.get_suffix(), start_index)
            icing_make_skb_time = float((line[start_index: end_index]).strip())
            self.icing_make_skb_times.append(icing_make_skb_time)
        elif SpecificPrefix.get_icing_forward_prefix() in line:
            start_index = (line.find(SpecificPrefix.get_icing_forward_prefix()) +
                           len(SpecificPrefix.get_icing_forward_prefix()))
            end_index = line.find(SpecificPrefix.get_suffix(), start_index)
            icing_forward_skb_time = float((line[start_index: end_index]).strip())
            self.icing_forward_skb_times.append(icing_forward_skb_time)

    def resolve_kernel_log_file(self):
        with open(self.kernel_log_file_path) as f:
            all_lines = f.readlines()
        for line in all_lines:
            self.analyze_single_line(line)

    def plot_distribution(self):
        """
        进行直方图的绘制
        :return:
        """
        plt.hist(self.opt_make_skb_times, bins=self.bins, color=Color.blue(), label="OPT (skb make time)",
                 density=True, alpha=0.6)
        plt.hist(self.opt_forward_skb_times, bins=self.bins, color=Color.green(), label="OPT (skb forward time)",
                 density=True, alpha=0.6)
        plt.hist(self.icing_make_skb_times, bins=self.bins, color=Color.orange(), label="ICING (skb make time)",
                 density=True, alpha=0.6)
        plt.hist(self.icing_forward_skb_times, bins=self.bins, color="purple", label="ICING (skb forward time)",
                 density=True, alpha=0.6)

    def plot_figure(self):
        self.resolve_kernel_log_file()
        plt.style.use("ieee")
        plt.figure(figsize=(7, 3.5), dpi=100)
        font = {
            "family": "sans-serif",
            "sans-serif": "Helvetica",
            "weight": "normal",
            "size": 10
        }
        plt.rc("font", **font)
        self.plot_distribution()
        plt.xlabel(u"Time Consumption of Forwarding (\u03bcs)", fontsize=13)
        plt.ylabel("Probability Density ($\\times10^{-4}$)", fontsize=13)
        # plt.xticks(np.arange(0, 5500, 1000), np.arange(0, 6, 1), fontsize=13)
        # plt.yticks(np.arange(0.0000, 0.0031, 0.0005), np.arange(0, 31, 5), fontsize=13)
        plt.legend()
        plt.tight_layout()
        with PdfPages(self.output_figure_name) as pdf:
            pdf.savefig()


if __name__ == "__main__":
    min_x = int(input("请输入启始值:"))
    max_x = int(input("请输入终止值:"))
    kernel_file_name = input("请输入要分析的文件名:")
    output_file_name = input("请输入输出的文件名:")
    forwarding_time_plotter_final = ForwardingTimePlotterFinal(
        kernel_log_file_path=f"../../resources/results/{kernel_file_name}",
        output_figure_name=f"{output_file_name}.pdf",
        min_x=min_x,
        max_x=max_x)
    forwarding_time_plotter_final.resolve_kernel_log_file()
    forwarding_time_plotter_final.plot_figure()
