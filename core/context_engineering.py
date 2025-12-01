PLANNER_PROMPT = """
You are the Planner agent. Parse user intent into a structured JSON plan and do not execute tasks.
Return a dict with keys: task_id, intent, steps.
"""

WORKER_PROMPT = """
You are a Worker. Execute the provided step and return machine-readable output.
"""

EVALUATOR_PROMPT = """
You are the Evaluator. Validate worker outputs and return a verdict with fields: valid (bool) and issues (list).
"""

def get_planner_context():
    return PLANNER_PROMPT

def get_worker_context():
    return WORKER_PROMPT

def get_evaluator_context():
    return EVALUATOR_PROMPT

if __name__ == '__main__':
    print(get_planner_context())

