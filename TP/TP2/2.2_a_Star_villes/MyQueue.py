import heapq
from typing import List, Tuple
from CityLink import *


class MyQueue:
    """ Queue heapq wrapper
    """

    def __init__(self):
        self.queue: List[Tuple[float, City]] = []

    def __iter__(self):
        return iter(self.queue)

    def __contains__(self, element):
        return element in self.queue

    def get(self):
        return heapq.heappop(self.queue)[1]

    def put(self, priority: int, element: City):
        heapq.heappush(self.queue, (priority, element))
