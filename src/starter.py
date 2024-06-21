if __name__ == "__main__":
    import sys
    sys.path.append("../")
from src.config import config_loader as clm
from src.interact import topology_manager as tmm
from loguru import logger

if __name__ == "__main__":
    config_loader_tmp = clm.ConfigLoader()
    config_loader_tmp.load(configuration_file_path="../resources/config.yaml")
    topology_manager = tmm.TopologyManager(config_loader=config_loader_tmp, logger=logger)
    topology_manager.topology_management()
