#!/usr/bin/env python3
"""
This module contains the MRUCache class.
This class inherits from the BaseCaching class in base_caching
"""
from base_caching import BaseCaching
from functools import reduce


class MRUCache(BaseCaching):
    """
    This class describes a MRUCache object.

    """

    def __init__(self):
        super().__init__()
        self._age_bit = -1
        self._age_dict = {}

    def put(self, k, item):
        """ Add an item in the cache
        Must assign to the dictionary self.cache_data the item value
        for the key.
        If key or item is None, this method should not do anything.
        """
        if k is None or item is None:
            return
        if k not in self.cache_data and len(self.cache_data) >= self.MAX_ITEMS:
            to_pop = reduce(lambda x, y: x if self._age_dict[x] >
                            self._age_dict[y] else y, self._age_dict)

            self.cache_data.pop(to_pop)
            self._age_dict.pop(to_pop)

            print("DISCARD: {}".format(to_pop))

        self._age_bit += 1
        self._age_dict[k] = self._age_bit

        self.cache_data[k] = item

    def get(self, key):
        """ Get an item by key
        Must return the value in self.cache_data linked to key.
        If key is None or if the key doesn’t exist in self.cache_data,
        return None.
        """
        if key in self.cache_data and key is not None:
            self._age_bit += 1
            self._age_dict[key] = self._age_bit

        return self.cache_data.get(key)
