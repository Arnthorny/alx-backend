#!/usr/bin/env python3
"""
This module contains the LFUCache class.
This class inherits from the BaseCaching class in base_caching
"""
from base_caching import BaseCaching
from functools import reduce


class LFUCache(BaseCaching):
    """
    This class describes a LFUCache object.

    """

    def __init__(self):
        super().__init__()
        self._age_bit = -1
        self._age_dict = {}
        self._freq_dict = {}

    def put(self, k, item):
        """ Add an item in the cache
        Must assign to the dictionary self.cache_data the item value
        for the key.
        If key or item is None, this method should not do anything.
        """
        if k is None or item is None:
            return
        if k not in self.cache_data and len(self.cache_data) >= self.MAX_ITEMS:
            least_fre = min(self._freq_dict.values())
            least_freq_item = [it[0] for it in self._freq_dict.items() if it[1]
                               == least_fre]
            to_pop = least_freq_item[0]

            # Use LRU algo if there are multi items to discard
            if len(least_freq_item) > 1:
                to_pop = reduce(lambda x, y: x if self._age_dict[x] <
                                self._age_dict[y] else y, least_freq_item)

            self.cache_data.pop(to_pop)
            self._age_dict.pop(to_pop)
            self._freq_dict.pop(to_pop)

            print("DISCARD: {}".format(to_pop))

        self._age_bit += 1
        self._freq_dict[k] = self._freq_dict.get(k, 0) + 1
        self._age_dict[k] = self._age_bit

        self.cache_data[k] = item

    def get(self, key):
        """ Get an item by key
        Must return the value in self.cache_data linked to key.
        If key is None or if the key doesn’t exist in self.cache_data,
        return None.
        """
        if key in self.cache_data and key is not None:
            self._freq_dict[key] = self._freq_dict.get(key, 0) + 1
            self._age_bit += 1
            self._age_dict[key] = self._age_bit

        return self.cache_data.get(key)
