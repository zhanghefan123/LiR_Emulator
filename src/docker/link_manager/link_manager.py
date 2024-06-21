from typing import List
from src.entities import satellite as sm


class LinkManager:
    def __init__(self, satellites: List[sm.Satellite]):
        self.satellites = satellites
