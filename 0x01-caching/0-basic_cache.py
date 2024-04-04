#!/usr/bin/env python3
"""
This module contains the BasicCache class.
This class inherits from the BaseCaching class in base_caching
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    This class describes a BasicCache object.

    This caching system doesn’t have limit
    """

    def __init__(self):
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache
        Must assign to the dictionary self.cache_data the item value
        for the key key.
        If key or item is None, this method should not do anything.
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        Must return the value in self.cache_data linked to key.
        If key is None or if the key doesn’t exist in self.cache_data,
        return None.
        """
        return self.cache_data.get(key)
