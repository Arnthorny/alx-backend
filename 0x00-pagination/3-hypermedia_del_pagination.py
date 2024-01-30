#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination

Implement a get_hyper_index method with two integer arguments: index with a
None default value and page_size with default value of 10.

The method should return a dictionary with the following key-value pairs:
index: the current start index of the return page. That is the index of the
first item in the current page. For example if requesting page 3 with page_size
20, and no data was removed from the dataset, the current index should be 60.
next_index: the next index to query with. That should be the index of the first
item after the last item on the current page.
page_size: the current page size
data: the actual page of the dataset
"""

import csv
import math
from typing import List, Union, Dict

ValueType = Union[int, List[List], None]


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Description:
        The goal here is that if between two queries, certain rows are removed
        from the dataset, the user does not miss items from dataset when
        changing page.
        """
        req_d: Dict[str, ValueType] = {}
        all_idxd_data = self.indexed_dataset()

        idx = index
        tmp_d: List = []
        assert (type(idx) == int and idx >= 0 and idx < len(all_idxd_data))
        for k, v in all_idxd_data.items():
            if len(tmp_d) == (page_size + 1):
                break
            if k >= idx:
                tmp_d.append((k, v))

        req_d['index'] = idx
        next_index = tmp_d.pop()[0] if len(tmp_d) > page_size else None
        req_d['next_index'] = next_index
        req_d['data'] = [v for k, v in tmp_d]
        req_d['page_size'] = len(tmp_d)

        return req_d
