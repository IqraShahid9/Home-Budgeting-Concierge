from typing import Dict, Any
from project.agents.planner import Planner
from project.agents.worker import WorkerHub
from project.agents.evaluator import Evaluator
from project.memory.session_memory import SessionMemory
from project.core.observability import SimpleLogger

class MainAgent:
    def __init__(self):
        self.memory = SessionMemory()
        self.logger = SimpleLogger('project/project_log.json')
        self.planner = Planner(memory=self.memory, logger=self.logger)
        self.worker_hub = WorkerHub(memory=self.memory, logger=self.logger)
        self.evaluator = Evaluator(memory=self.memory, logger=self.logger)

    def handle_message(self, user_input: str) -> Dict[str, Any]:
        plan_msg = self.planner.plan(user_input)
        data = {}
        rows = self.memory.get('uploaded_rows', [])
        data['rows'] = rows
        plan_msg['payload']['data'] = data
        worker_results = self.worker_hub.handle(plan_msg)
        # Merge summary if missing overall
        if 'totals' in worker_results and 'overall' not in worker_results:
            worker_results['overall'] = sum(worker_results['totals'].values())
        verdict = self.evaluator.validate(plan_msg.get('payload',{}).get('plan',{}), worker_results)
        if not verdict.get('valid'):
            response = {'status':'error', 'issues': verdict.get('issues')}
        else:
            response = {'status':'ok', 'response': worker_results}
        self.logger.log({'agent':'main','user_input': user_input, 'outcome': response})
        return {'response': response}

def run_agent(user_input: str):
    agent = MainAgent()
    result = agent.handle_message(user_input)
    return result["response"]

if __name__ == '__main__':
    print(run_agent('Hello from main'))

