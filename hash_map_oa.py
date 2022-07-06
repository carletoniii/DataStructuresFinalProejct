# Name: Carleton Barrett Foster III
# OSU Email: fostcarl@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3 June 2022
# Description: Implementation of the HashMap class with open addressing


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
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
        This method updates the key / value pair in the hash map. If the given key already exists in the hash map, its
        associated value must be replaced with the new value. If the given key is not in the hash map, a key / value
        pair must be added.
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)
        hash = self._hash_function(key)
        index = hash % self._capacity
        j = 1
        current_index = self._buckets.get_at_index(index)
        while current_index != None:
            if current_index.key == key:
                break
            elif current_index.is_tombstone == True:
                break
            else:
                index = (hash + j ** 2) % self._capacity
                j += 1
                current_index = self._buckets.get_at_index(index)
        if current_index != None and current_index.is_tombstone == False:
            if current_index.key == key:
                self._buckets.set_at_index(index, HashEntry(key, value))
                return
        elif current_index != None and current_index.is_tombstone == True:
            if current_index.key == key:
                self._buckets.set_at_index(index, HashEntry(key, value))
                self._size += 1
                return
        else:
            self._buckets.set_at_index(index, HashEntry(key, value))
            self._size += 1
            return

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        empty_buckets = 0
        for x in range(self._capacity):
            if self._buckets.get_at_index(x) == None:
                empty_buckets += 1
            elif self._buckets.get_at_index(x).is_tombstone == True:
                empty_buckets += 1
            else:
                continue
        return empty_buckets

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. All existing key / value pairs must remain in the
        new hash map, and all hash table links must be rehashed. If new_capacity is less than 1, or less than the
        current number of elements in the map, the method does nothing.
        """
        # remember to rehash non-deleted entries into new table
        if new_capacity < 1 or new_capacity < self._size:
            return
        else:
            old_buckets = self._buckets
            self._buckets = DynamicArray()
            for _ in range(new_capacity):
                self._buckets.append(None)
            self._capacity = new_capacity
            self._size = 0
            for i in range(old_buckets.length()):
                current_entry = old_buckets.get_at_index(i)
                if current_entry == None:
                    continue
                elif current_entry.is_tombstone == True:
                    continue
                else:
                    self.put(current_entry.key, current_entry.value)
        return

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key is not in the hash map, the method
        returns None.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        j = 1
        current_index = self._buckets.get_at_index(index)
        while current_index != None:
            if current_index.key == key and current_index.is_tombstone == False:
                return current_index.value
            else:
                index = (hash + j ** 2) % self._capacity
                j += 1
                current_index = self._buckets.get_at_index(index)
        return None

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False. An empty hash map does
        not contain any keys.
        """
        if self._size == 0:
            return False
        else:
            hash = self._hash_function(key)
            index = hash % self._capacity
            j = 1
            current_index = self._buckets.get_at_index(index)
            while current_index != None:
                if current_index.key == key and current_index.is_tombstone == False:
                    return True
                else:
                    index = (hash + j ** 2) % self._capacity
                    j += 1
                    current_index = self._buckets.get_at_index(index)
            return False

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map. If the key is not in the hash map,
        the method does nothing (no exception needs to be raised).
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        j = 1
        current_index = self._buckets.get_at_index(index)
        while current_index != None:
            if current_index.key == key and current_index.is_tombstone == False:
                self._buckets.get_at_index(index).is_tombstone = True
                self._size -= 1
                return
            else:
                index = (hash + j ** 2) % self._capacity
                j += 1
                current_index = self._buckets.get_at_index(index)
        return

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash table capacity.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0
        return

    def get_keys(self) -> DynamicArray:
        """
        This method returns a DynamicArray that contains all the keys stored in the hash map. The order of the keys in
        the DA does not matter.
        """
        DA = DynamicArray()
        if self._size == 0:
            return DA
        else:
            for x in range(self._capacity):
                if self._buckets.get_at_index(x) != None:
                    if self._buckets.get_at_index(x).is_tombstone == False:
                        DA.append(self._buckets.get_at_index(x).key)
            return DA


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
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
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

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

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
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
    m = HashMap(75, hash_function_2)
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
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
