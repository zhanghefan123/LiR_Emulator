import numpy
import scipy.stats as stats
import scienceplots
import math
import os
import numpy as np
import matplotlib
import matplotlib.style as style
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


class SpecificPrefix:

    @classmethod
    def get_lir_reencoding_prefix(cls):
        return "LiR Reencoding Forward Time Consumption: "

    @classmethod
    def get_lir_prefix(cls):
        return "LiR Direct Forward Time Consumption: "

    @classmethod
    def get_ip_prefix(cls):
        return "ip rcv take"

    @classmethod
    def get_lir_suffix(cls):
        return "ns"

    @classmethod
    def get_ip_suffix(cls):
        return "ns"


class ForwardingTimePlotter:  # LiR Forward Time Consumption
    def __init__(self, kernel_log_file_path: str, output_figure_name: str, start, end):
        self.kernel_log_file_path = kernel_log_file_path
        self.output_figure_name = output_figure_name
        self.lir_forwarding_time_list = []
        self.ip_forwarding_time_list = []
        self.lir_reencoding_time_list = []
        self.bins = np.arange(start, end, 25)

    def resolve_kernel_log_file(self):
        with open(self.kernel_log_file_path) as f:
            lines = f.readlines()
        for line in lines:
            try:
                if SpecificPrefix.get_lir_prefix() in line:
                    start_index = line.find(SpecificPrefix.get_lir_prefix()) + len(SpecificPrefix.get_lir_prefix())
                    end_index = line.find(SpecificPrefix.get_lir_suffix(), start_index)
                    lir_forwarding_time = float((line[start_index: end_index]).strip())
                    self.lir_forwarding_time_list.append(lir_forwarding_time)
                elif SpecificPrefix.get_ip_prefix() in line:
                    start_index = line.find(SpecificPrefix.get_ip_prefix()) + len(SpecificPrefix.get_ip_prefix())
                    end_index = line.find(SpecificPrefix.get_ip_suffix(), start_index)
                    lir_forwarding_time = float((line[start_index: end_index]).strip())
                    self.ip_forwarding_time_list.append(lir_forwarding_time)
                elif SpecificPrefix.get_lir_reencoding_prefix() in line:
                    start_index = line.find(SpecificPrefix.get_lir_reencoding_prefix()) + len(SpecificPrefix.get_lir_reencoding_prefix())
                    end_index = line.find(SpecificPrefix.get_lir_suffix(), start_index)
                    lir_reencoding_forwarding_time = float((line[start_index: end_index]).strip())
                    self.lir_reencoding_time_list.append(lir_reencoding_forwarding_time)
                else:
                    pass  # 内核之中其他的输出行
            except ValueError:
                print(line)

    def plot_distribution(self):
        plt.hist(self.lir_forwarding_time_list, bins=self.bins, color="blue", label="LiR (direct forwarding)", density=True, alpha=0.5)
        plt.hist(self.lir_reencoding_time_list, bins=self.bins, color="red", label="LiR (re-encoding)", density=True, alpha=0.5)
        plt.hist(self.ip_forwarding_time_list, bins=self.bins, color="orange", label="ip", density=True, alpha=0.5)

    def plot_figure(self):
        self.resolve_kernel_log_file()
        plt.style.use("ieee")
        plt.figure(figsize=(4.3, 2.8), dpi=100)
        font = {
            "family": "sans-serif",
            "sans-serif": "Helvetica",
            "weight": "normal",
            "size": 10
        }
        plt.rc("font", **font)
        self.plot_distribution()
        plt.xlabel(u"Time Consumption of Forwarding (ns)", fontsize=13)
        plt.ylabel("Probability Density", fontsize=13)
        plt.legend()
        plt.tight_layout()
        with PdfPages(self.output_figure_name) as pdf:
            pdf.savefig()


if __name__ == "__main__":
    start = int(input("请输入起始值:"))
    end = int(input("请输入终止值:"))
    kern_file_name = input("请输入要分析的文件名:")
    plot_file_name = input("请输入输出的pdf名:")
    forwarding_time_plotter = ForwardingTimePlotter(kernel_log_file_path=f"../../resources/{kern_file_name}",
                                                    output_figure_name=f"{plot_file_name}.pdf",
                                                    start=start,
                                                    end=end)
    forwarding_time_plotter.plot_figure()
