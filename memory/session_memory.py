import time
from typing import Any, Dict

class SessionMemory:
    def __init__(self):
        self._store = {}

    def set(self, key: str, value: Any) -> None:
        self._store[key] = {'value': value, 'ts': time.time()}

    def get(self, key: str, default=None):
        item = self._store.get(key)
        if not item:
            return default
        return item.get('value')

    def clear(self):
        self._store = {}

    def dump(self):
        return {k:v['value'] for k,v in self._store.items()}

if __name__ == '__main__':
    m = SessionMemory()
    m.set('a',1)
    print(m.get('a'))

