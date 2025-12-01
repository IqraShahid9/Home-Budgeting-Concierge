from typing import Dict, Any
import uuid
from project.core.a2a_protocol import Message
from project.core.observability import SimpleLogger

class Planner:
    def __init__(self, memory=None, logger=None):
        self.memory = memory
        self.logger = logger or SimpleLogger('project/project_log.json')

    def _new_task_id(self) -> str:
        return str(uuid.uuid4())

    def plan(self, user_input: str) -> Dict[str, Any]:
        intent = 'summarize'
        ui = user_input.lower()
        if any(w in ui for w in ['forecast','predict','upcoming','next']):
            intent = 'forecast'
        if any(w in ui for w in ['categor','category','categorize']):
            intent = 'categorize'
        if any(w in ui for w in ['budget','save','saving','recommend']):
            intent = 'recommend'
        task_id = self._new_task_id()
        plan = {
            'task_id': task_id,
            'intent': intent,
            'user_input': user_input,
            'steps': []
        }
        if intent == 'categorize':
            plan['steps'].append({'worker': 'categorizer', 'action': 'categorize'})
        elif intent == 'forecast':
            plan['steps'].append({'worker': 'categorizer', 'action': 'categorize'})
            plan['steps'].append({'worker': 'forecast', 'action': 'forecast'})
        elif intent == 'recommend':
            plan['steps'].append({'worker': 'categorizer', 'action': 'categorize'})
            plan['steps'].append({'worker': 'summary', 'action': 'summarize'})
            plan['steps'].append({'worker': 'forecast', 'action': 'forecast'})
        else:
            plan['steps'].append({'worker': 'categorizer', 'action': 'categorize'})
            plan['steps'].append({'worker': 'summary', 'action': 'summarize'})

        message = Message(
            sender='planner',
            receiver='workers',
            task_id=task_id,
            intent=plan['intent'],
            payload={'plan': plan},
            requires_memory=True,
            memory_keys=['uploaded_rows','recurring_bills','budget_goals']
        )
        self.logger.log({'agent': 'planner', 'action': 'plan_created', 'plan': plan})
        return message.to_dict()

if __name__ == '__main__':
    p = Planner()
    print(p.plan('Summarize my last month'))

