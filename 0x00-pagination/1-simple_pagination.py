#!/usr/bin/env python3
"""
Implement a method named get_page that takes two integer arguments page with
default value 1 and page_size with default value 10.

You have to use this CSV file (same as the one presented at the top of the
project)
Use assert to verify that both arguments are integers greater than 0.
Use index_range to find the correct indexes to paginate the dataset correctly
and return the appropriate page of the dataset (i.e. the correct list of rows).
If the input arguments are out of range for the dataset, an empty list should
be returned.
"""
import csv
import math
from typing import List, Tuple


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
