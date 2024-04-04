#!/usr/bin/env python3
"""
This module contains the FIFOCache class.
This class inherits from the BaseCaching class in base_caching
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    This class describes a BasicCache object.

    """

    def __init__(self):
        super().__init__()

    def put(self, k, item):
        """ Add an item in the cache
        Must assign to the dictionary self.cache_data the item value
        for the key.
        If key or item is None, this method should not do anything.
        """
        if k is None or item is None:
            return
        if k not in self.cache_data and len(self.cache_data) >= self.MAX_ITEMS:
            discarded = list(self.cache_data.keys())[0]
            self.cache_data.pop(discarded)

            print("DISCARD: {}".format(discarded))

        self.cache_data[k] = item

    def get(self, key):
        """ Get an item by key
        Must return the value in self.cache_data linked to key.
        If key is None or if the key doesn’t exist in self.cache_data,
        return None.
        """
        return self.cache_data.get(key)
