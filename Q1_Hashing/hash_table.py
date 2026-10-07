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

    def locate (self, key):
        """Return (slot index, probes) for key, or (None, probes) if absent."""
        idx = self._hash(key)
        start = idx
        probes = 1
        while True:
            slot = self._slots[idx]
            if slot is None:
                return None, probes
            if slot is not _TOMBSTONE and slot.key == key:
                return idx, probes
            idx = (idx + 1) % self._capacity
            if idx == start:
                return None, probes
            probes += 1

    def search(self, key):
        """Return the value stored for key. Raise KeyError if absent."""
        idx, _ = self.locate(key)
        if idx is None:
            raise KeyError(key)
        return self._slots[idx].value

    def update(self, key, value):
        """Replace the value for an existing key. Raise KeyError if absent."""
        idx, _ = self.locate(key)
        if idx is None:
            raise KeyError(key)
        self._slots[idx].value = value
        return idx

    def delete(self, key):
        """Remove key, leaving a tombstone. Return the removed value"""
        idx, _ = self.locate(key)
        if idx is None:
            raise KeyError(key)
        value = self._slots[idx].value
        self._slots[idx] = _TOMBSTONE
        self._size -= 1
        return value

    def display(self):
        """Print every slot's state (for testing and reporting purposes)"""
        for i, slot in enumerate(self._slots):
            if slot is None:
                state = "empty"
            elif slot is _TOMBSTONE:
                state = "tombstone"
            else:
                state = f"{slot.key!r} -> {slot.value!r}"
            print(f"[{i}] {state}")

if __name__ == "__main__":
    table = HashTable(7)
    for key, value in [(10, "A"), (17, "B"), (24, "C")]:
        table.insert(key, value)

    print("Deleted 17, value was:", table.delete(17))
    print("Locate 24 (slot, probes):", table.locate(24))
    print("Search 24:", table.search(24))

    table.update(24, "C-new")
    print("After update, search 24:", table.search(24))
    print("Delete 24:", table.delete(24))

    try:
        table.search(24)
    except KeyError as error:
        print("Search 24 after delete -> not found:", error)

    print("Insert 31 -> slot", table.insert(31, "D"))
    print("Size:", len(table), "| Load factor:", round(table.load_factor(), 2))
    table.display()