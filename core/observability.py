import json
import time
from typing import Dict, Any

class SimpleLogger:
    def __init__(self, path='project/project_log.json'):
        self.path = path
        try:
            with open(self.path, 'r') as f:
                pass
        except Exception:
            with open(self.path, 'w') as f:
                json.dump([], f)

    def log(self, entry: Dict[str, Any]) -> None:
        record = {'ts': time.time(), **entry}
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
        except Exception:
            data = []
        data.append(record)
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=2)

if __name__ == '__main__':
    logger = SimpleLogger()
    logger.log({'agent':'test','action':'ping'})

