# Name: Amadou Diallo
# OSU Email: dialloam@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/14/24
# Description: Implementing a hashmap class using a dynamic array to store the table.
# Open Addressing with Quadratic probing was implemented. Average time complexity is O(1).
# Dynamic array was used to store OA hash table. the number of objects are from 0 to 1 million.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        # Check for load factor and resizing
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)
        index = self._hash_function(key)
        # Quadratic probing, increment size if tombstone or empty, and associated key
        for j in range(self._capacity):
            quadratic_probe = (index + j ** 2) % self._capacity
            buckets = self._buckets[quadratic_probe]
            if buckets is None or buckets.is_tombstone:
                self._buckets.set_at_index(quadratic_probe, HashEntry(key, value))
                self._size = self._size + 1
                return
            elif buckets.key == key:
                self._buckets.set_at_index(quadratic_probe, HashEntry(key, value))
                return

    def resize_table(self, new_capacity: int) -> None:
        """
        function that changes the capacity of the table
        """
        if new_capacity < self._size:
            return
        # Check for prime
        while not self._is_prime(new_capacity):
            new_capacity = new_capacity + 1
        resized_table = HashMap(new_capacity, self._hash_function)
        # All pairs from previous to resized table
        for elements in self:
            if elements is not None:
                e_key, value = elements.key, elements.value
                resized_table.put(e_key, value)
        # Updates
        self._buckets = resized_table._buckets
        self._size = resized_table._size
        self._capacity = resized_table._capacity

    def table_load(self) -> float:
        """
        function that returns the current load factor
        """
        return float(self._size) / self._capacity

    def empty_buckets(self) -> int:
        """
        function that returns number of empty buckets
        """
        return int(self._capacity - self._size)

    def get(self, key: str) -> object:
        """
        function that returns value of corresponding key
        """
        # Using a for loop to iterate the buckets then check for empty, tombstone, and corresponding value
        for index in range(self._buckets.length()):
            bucket = self._buckets[index]
            if bucket is not None:
                if bucket.is_tombstone:
                    continue
                if bucket.key == key:
                    return bucket.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        function that returns True if the key is present, otherwise False
        """
        # Using a for loop to iterate the buckets then check for empty, tombstone, and corresponding value
        for index in range(self._buckets.length()):
            bucket = self._buckets[index]
            if bucket is not None:
                if bucket.is_tombstone:
                    continue
                if bucket.key == key:
                    return True
        return False

    def remove(self, key: str) -> None:
        """
        function that removes the key and its value
        """
        # Using a for loop to iterate each bucket, check corresponding key, then decrement size
        for index in range(self._capacity):
            bucket = self._buckets[index]
            if bucket and bucket.key == key and not bucket.is_tombstone:
                bucket.is_tombstone = True
                self._size = self._size - 1
                return

    def get_keys_and_values(self) -> DynamicArray:
        """
        function that returns a dynamic array that contains a tuple
        """
        keys_values = DynamicArray()
        # Using a for loop to iterate each bucket, check empty or tombstone, then append tuple
        for index in range(self._buckets.length()):
            buckets = self._buckets[index]
            if buckets is not None:
                if buckets.is_tombstone is False:
                    keys_values.append((buckets.key, buckets.value))
        return keys_values

    def clear(self) -> None:
        """
         function that clears the contents of the hash
        """
        # Dynamic array is put at size 0 and cleared
        self._buckets = DynamicArray()
        self._size = 0
        for contents in range(self._capacity):
            self._buckets.append(None)

    def __iter__(self):
        """
        function that allows the hash map to self-iterate
        """
        self.index = 0
        return self

    def __next__(self):
        """
        function that returns the next item based on current index of iterator
        """
        try:
            # Using a while loop to move to the next index and check if the value is empty or tombstone.
            while True:
                value = self._buckets.get_at_index(self.index)
                self.index = self.index + 1
                if value is not None and not value.is_tombstone:
                    return value
        except DynamicArrayException:
            raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

