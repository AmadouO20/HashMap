# Name: Amadou Diallo
# OSU Email: dialloam@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/14/24
# Description: Implementing a hashmap class using a dynamic array to store the table.
# Chaining for collision resolution was implemented. Average time complexity is O(1).
# Dynamic array was used to store SC hash table. the number of objects are from 0 to 1 million.

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        function that updates key and value pair
        """
        # Check load factor
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)
        h_value = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(h_value)
        index = bucket.contains(key)
        # Update/Insert key and value pair
        if index:
            index.value = value
        else:
            bucket.insert(key, value)
            self._size = self._size + 1

    def resize_table(self, new_capacity: int) -> None:
        """
        function that changes the capacity of the table
        """
        if new_capacity < 1:
            return
        # Check for prime
        if self._capacity == 2:
            new_capacity = 2
        else:
            if new_capacity >= 1:
                if not self._is_prime(new_capacity):
                    new_capacity = self._next_prime(new_capacity)
        buckets = DynamicArray()
        # Using a for loop to iterate through the table, check if its empty, and the linked list
        for a in range(new_capacity):
            buckets.append(LinkedList())
        for index in range(self._buckets.length()):
            bucket = self._buckets[index]
            for node in bucket:
                h_value = self._hash_function(node.key) % new_capacity
                buckets[h_value].insert(node.key, node.value)
        # Updates
        self._buckets = buckets
        self._capacity = new_capacity

    def table_load(self) -> float:
        """
        function that returns the current load factor
        """
        return float(self._size) / self._capacity

    def empty_buckets(self) -> int:
        """
        function that returns the number of empty buckets
        """
        empty = 0
        index = 0
        # Using a while loop to check if the bucket is empty
        while index < self._capacity:
            if self._buckets.get_at_index(index).length() == 0:
                empty = empty + 1
            index = index + 1
        return empty

    def get(self, key: str):
        """
        function that returns value corresponding to key
        """
        value = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(value)
        # Check the list and iterate it
        if bucket.length() > 0:
            for node in bucket:
                if node.key == key:
                    return node.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        function that returns True if the key is present, otherwise False
        """
        # iterate buckets and check if its empty, then check if the key is associated
        value = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(value)
        if bucket.length() > 0:
            for node in bucket:
                if node.key == key:
                    return True
        return False

    def remove(self, key: str) -> None:
        """
        function that removes the key and its value
        """
        # Using a for loop to iterate each bucket, check if empty, then check if corresponding
        for bucket in range(self._capacity):
            curr_bucket = self._buckets.get_at_index(bucket)
            if curr_bucket.length() > 0:
                for value in curr_bucket:
                    if value.key == key:
                        curr_bucket.remove(key)
                        self._size = self._size - 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        function that returns a dynamic array that contains a tuple
        """
        keys_values = DynamicArray()
        # Using a for loop to traverse bucket in the hash map and each node in the linked list
        for bucket in range(self._buckets.length()):
            for node in self._buckets.get_at_index(bucket):
                keys_values.append((node.key, node.value))
        return keys_values

    def clear(self) -> None:
        """
        function that clears the contents of the hash
        """
        # Dynamic array is put at size 0 and cleared
        self._buckets = DynamicArray()
        for contents in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def contents_buckets(self):
        """Function that is used with find_mode"""
        for contents in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(contents)
            if bucket:
                yield bucket


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    function that returns a tuple containing the mode, and the maximum frequency from a dynamic array
    """
    map = HashMap()
    # Using a for loop for the frequency and increments it
    for frequencies in range(da.length()):
        element = da.get_at_index(frequencies)
        if map.contains_key(element):
            map.put(element, map.get(element) + 1)
        else:
            map.put(element, 1)
    maximum_frequency = 0
    mode_element = DynamicArray()
    # Using a for loop to find the maximum, update the frequency, and update the mode of elements
    for bucket in map.contents_buckets():
        for node in bucket:
            element, occurrence = node.key, node.value
            if occurrence > maximum_frequency:
                maximum_frequency = occurrence
                mode_element = DynamicArray([element])
            elif occurrence == maximum_frequency:
                mode_element.append(element)
    return mode_element, maximum_frequency

# ------------------- BASIC TESTING ---------------------------------------- #



