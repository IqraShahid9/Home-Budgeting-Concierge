from typing import Dict, Any, List
from project.tools.tools import (
    parse_csv_rows,
    categorize_transactions,
    build_monthly_summary,
    forecast_recurring_bills
)
from project.core.observability import SimpleLogger

class ExpenseCategorizer:
    def __init__(self, memory=None, logger=None):
        self.memory = memory
        self.logger = logger or SimpleLogger('project/project_log.json')

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        rows = payload.get('rows') or []
        categories = categorize_transactions(rows)
        self.logger.log({'agent': 'categorizer', 'count': len(categories)})
        return {'categories': categories}

class MonthlySummaryBuilder:
    def __init__(self, memory=None, logger=None):
        self.memory = memory
        self.logger = logger or SimpleLogger('project/project_log.json')

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        categories = payload.get('categories') or []
        summary = build_monthly_summary(categories)
        self.logger.log({'agent': 'summary_builder', 'totals': summary.get('totals',{})})
        return summary

class ForecastGenerator:
    def __init__(self, memory=None, logger=None):
        self.memory = memory
        self.logger = logger or SimpleLogger('project/project_log.json')

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        categories = payload.get('categories') or []
        forecast = forecast_recurring_bills(categories)
        self.logger.log({'agent': 'forecast_generator', 'forecast_items': len(forecast)})
        return {'forecast': forecast}

class WorkerHub:
    def __init__(self, memory=None, logger=None):
        self.categorizer = ExpenseCategorizer(memory, logger)
        self.summary_builder = MonthlySummaryBuilder(memory, logger)
        self.forecast_generator = ForecastGenerator(memory, logger)

    def handle(self, message: Dict[str, Any]) -> Dict[str, Any]:
        plan = message.get('payload', {}).get('plan', {})
        steps = plan.get('steps', [])
        intermediate = {}
        # Attach provided data rows if any
        data = message.get('payload', {}).get('data', {})
        rows = data.get('rows', [])
        for step in steps:
            worker = step.get('worker')
            action = step.get('action')
            if worker == 'categorizer':
                res = self.categorizer.run({'rows': rows})
                intermediate.update(res)
            elif worker == 'summary':
                res = self.summary_builder.run({'categories': intermediate.get('categories', [])})
                intermediate.update(res)
            elif worker == 'forecast':
                res = self.forecast_generator.run({'categories': intermediate.get('categories', [])})
                intermediate.update(res)
        return intermediate

if __name__ == '__main__':
    print('Worker module loaded')

