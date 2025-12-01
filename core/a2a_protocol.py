from dataclasses import dataclass, asdict
from typing import Any, Dict, List

@dataclass
class Message:
    sender: str
    receiver: str
    task_id: str
    intent: str
    payload: Dict[str, Any]
    requires_memory: bool = False
    memory_keys: List[str] = None
    metadata: Dict[str,Any] = None

    def to_dict(self):
        return asdict(self)

if __name__ == '__main__':
    m = Message('planner','workers','tid','summarize',{'plan':{}})
    print(m.to_dict())

