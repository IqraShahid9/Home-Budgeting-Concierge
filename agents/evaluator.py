from typing import Dict, Any
from project.core.observability import SimpleLogger

class Evaluator:
    def __init__(self, memory=None, logger=None):
        self.memory = memory
        self.logger = logger or SimpleLogger('project/project_log.json')

    def validate(self, plan: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        issues = []
        if 'categories' not in results:
            issues.append('Missing categories in results')
        if any(s.get('action')=='forecast' for s in plan.get('steps',[])) and 'forecast' not in results:
            issues.append('Forecast requested but missing')
        # Basic math check
        totals = results.get('totals')
        if totals:
            overall = sum(totals.values())
            if abs(overall - results.get('overall', overall)) > 1e-6:
                issues.append('Totals mismatch')
        valid = len(issues) == 0
        verdict = {'valid': valid, 'issues': issues, 'results': results}
        self.logger.log({'agent': 'evaluator', 'verdict': verdict})
        return verdict

if __name__ == '__main__':
    e = Evaluator()
    print(e.validate({'steps':[]},{'categories':[], 'totals':{}, 'overall':0}))

