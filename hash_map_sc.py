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
        # Ensure new capacity is a prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Create a new dynamic array for the new buckets
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())
        
        # Save the old buckets
        old_buckets = self._buckets
        old_capacity = self._capacity
        
        # Update to new buckets and capacity
        self._buckets = new_buckets
        self._capacity = new_capacity
        self._size = 0  # Reset size, as put() will increment it

        # Rehash and insert all old key-value pairs into the new buckets
        for i in range(old_capacity):
            bucket = old_buckets.get_at_index(i)
            for node in bucket:
                self.put(node.key, node.value)

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

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
