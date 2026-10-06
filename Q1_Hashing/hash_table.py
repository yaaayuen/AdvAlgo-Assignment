"""Generic hash table using open addressing with linear probing"""
class _Entry:
    """One occupied slot: has a key and a value"""
    def __init__(self, key, value):
        self.key = key
        self.value = value

# Unique marker placed in a slot when its entry is deleted (tombstone).
_TOMBSTONE = object()

class HashTable:
    """Hash table that stores key-value pairs using linear probing"""
    def __init__(self, capacity=101):
        if capacity < 1:
            raise ValueError("Capacity must be greater than 0")
        self._capacity = capacity
        self._slots = [None] * capacity # None means empty, never used
        self._size = 0 # number of keys stored

    def __len__(self):
        return self._size

    def capacity(self):
        return self._capacity

    def load_factor(self):
        return self._size / self._capacity

    def _hash(self, key):
        """Return the home slot index for a key (int or str)"""
        if isinstance(key, int):
            return key % self._capacity
        if isinstance(key, str):
            total = 0
            for char in key:
                total = (total * 31 + ord(char)) % self._capacity
            return total
        raise TypeError(f"Unsupported key type: {type(key).__name__}")

    def insert(self, key, value):
        """Insert a new key-value pair and return the slot index used
        Raises ValueError if key is already present (duplicate)
        Raises OverflowError if table has no free slot"""
        idx = self._hash(key)
        start = idx
        first_tombstone = None

        while True:
            slot = self._slots[idx] # Reads the slot once
            if slot is None:
                break
            if slot is _TOMBSTONE:
                if first_tombstone is None:
                    first_tombstone = idx
            elif slot.key == key:
                raise ValueError(f"Key {key!r} already exists.")
            idx = (idx + 1) % self._capacity
            if idx == start:
                break

        if first_tombstone is not None:
            target = first_tombstone
        elif self._slots[idx] is None:
            target = idx
        else:
            raise OverflowError("Hash table is full.")

        self._slots[target] = _Entry(key, value)
        self._size += 1
        return target


if __name__ == "__main__":
    table = HashTable(7)
    print("10 ->", table.insert(10, "A"))
    print("17 ->", table.insert(17, "B"))
    print("24 ->", table.insert(24, "C"))

    # Pretend 17 was deleted (real delete comes in Piece 4)
    table._slots[4] = _TOMBSTONE
    table._size -= 1

    try:
        table.insert(24, "C2")
    except ValueError as error:
        print("Rejected:", error)

    print("31 ->", table.insert(31, "D"))