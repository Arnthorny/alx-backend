#!/usr/bin/env python3
"""
Implement a get_hyper method that takes the same arguments (and defaults) as
get_page and returns a dictionary containing the following key-value pairs:

page_size: the length of the returned dataset page
page: the current page number
data: the dataset page (equivalent to return from previous task)
next_page: number of the next page, None if no next page
prev_page: number of the previous page, None if no previous page
total_pages: the total number of pages in the dataset as an integer
"""
import csv
import math
from typing import List, Tuple, Dict, Union

ValueType = Union[str, int, List[List], None]


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Method that returns required page based on arguments given

        Args:
            page: Page number which are 1-indexed
            page_size: The size of each page

        Returns:
            (list): List containing rows in required page interval.
        """
        assert (type(page) == int and page > 0)
        assert (type(page_size) == int and page_size > 0)

        s, e = index_range(page, page_size)
        all_data = self.dataset()

        return all_data[s:e]

    def get_hyper(self, page: int = 1,
                  page_size: int = 10) -> Dict[str, ValueType]:
        """
        Method that takes the same arguments (and defaults) as get_page and
        returns a dictionary containing certain key-value pairs.
        """
        req_d: Dict[str, ValueType] = {}
        data = self.get_page(page, page_size)
        all_data = self.dataset()
        total_pages = math.ceil(len(all_data) / page_size)

        req_d['page_size'] = len(data)
        req_d['page'] = page
        req_d['data'] = data
        req_d['prev_page'] = page - 1 if page > 1 else None
        req_d['total_pages'] = total_pages
        req_d['next_page'] = page + 1 if page < total_pages else None

        return req_d


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate start and end index

    Args:
        page: Page number which are 1-indexed
        page_size: The size of each page

    Return:
        (tuple): Containing the start and end index.
    """
    end_index = page_size * page
    start_index = end_index - page_size

    return (start_index, end_index)
