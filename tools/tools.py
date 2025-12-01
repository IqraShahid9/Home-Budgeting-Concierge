from typing import List, Dict, Any
import csv

DEFAULT_CATEGORY_RULES = {
    'grocery': ['walmart', 'whole foods', 'costco', 'aldi', 'kroger'],
    'utilities': ['utility', 'electric', 'gas', 'water', 'electricity'],
    'subscription': ['netflix', 'spotify', 'amazon prime', 'hbo', 'disney'],
    'transport': ['uber', 'lyft', 'taxi', 'metro', 'train'],
    'dining': ['restaurant', 'cafe', 'starbucks', 'mcdonald']
}

def parse_csv_rows(csv_text: str) -> List[Dict[str,Any]]:
    rows = []
    try:
        reader = csv.DictReader(csv_text.splitlines())
        for r in reader:
            rows.append(r)
    except Exception:
        with open(csv_text, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append(r)
    return rows

def categorize_transactions(rows: List[Dict[str,Any]], rules: Dict[str,List[str]]=DEFAULT_CATEGORY_RULES) -> List[Dict[str,Any]]:
    categorized = []
    for r in rows:
        desc = (r.get('description') or r.get('merchant') or r.get('payee') or '').lower()
        try:
            amount = float(r.get('amount') or r.get('amt') or r.get('value') or 0)
        except Exception:
            amount = 0.0
        cat = 'other'
        for k, kws in rules.items():
            for kw in kws:
                if kw in desc:
                    cat = k
                    break
            if cat != 'other' and cat in rules:
                break
        categorized.append({'description': desc, 'amount': amount, 'category': cat, 'raw': r})
    return categorized

def build_monthly_summary(categories: List[Dict[str,Any]]) -> Dict[str,Any]:
    totals = {}
    for it in categories:
        c = it.get('category','other')
        totals[c] = totals.get(c, 0.0) + float(it.get('amount', 0.0))
    overall = sum(totals.values())
    return {'totals': totals, 'overall': overall}

def forecast_recurring_bills(categories: List[Dict[str,Any]]) -> List[Dict[str,Any]]:
    recurring = {}
    for it in categories:
        desc = it.get('description','')
        amt = it.get('amount',0.0)
        key = desc.strip()
        rec = recurring.get(key, {'amounts': []})
        rec['amounts'].append(amt)
        recurring[key] = rec
    out = []
    for k,v in recurring.items():
        avg = sum(v['amounts'])/len(v['amounts']) if v['amounts'] else 0.0
        out.append({'description': k, 'expected_amount': round(avg, 2)})
    return out

if __name__ == '__main__':
    print('Tools ready')

