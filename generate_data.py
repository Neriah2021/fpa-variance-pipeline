import pandas as pd
import numpy as np
import random
from datetime import date

random.seed(42)
np.random.seed(42)

departments = ['Sales', 'Marketing', 'Engineering', 'HR', 'Finance', 'Operations']
cost_categories = ['Salaries', 'Software', 'Travel', 'Office']
years = [2022, 2023, 2024]
months = range(1, 13)

rows = []
for year in years:
    for month in months:
        for dept in departments:
            for category in cost_categories:
                if category == 'Salaries':
                    base = {'Sales': 80000, 'Marketing': 60000, 'Engineering': 120000,
                            'HR': 40000, 'Finance': 50000, 'Operations': 70000}[dept]
                elif category == 'Software':
                    base = {'Sales': 5000, 'Marketing': 8000, 'Engineering': 20000,
                            'HR': 2000, 'Finance': 4000, 'Operations': 3000}[dept]
                elif category == 'Travel':
                    base = {'Sales': 15000, 'Marketing': 10000, 'Engineering': 3000,
                            'HR': 2000, 'Finance': 3000, 'Operations': 5000}[dept]
                else:
                    base = 3000

                budget = round(base * (1 + 0.05 * (year - 2022)) + random.uniform(-500, 500), 2)
                variance_pct = random.uniform(-0.15, 0.20)
                actuals = round(budget * (1 + variance_pct), 2)

                rows.append({
                    'year': year,
                    'month': month,
                    'department': dept,
                    'cost_category': category,
                    'budget': budget,
                    'actuals': actuals
                })

df = pd.DataFrame(rows)
df.to_csv('meridian_corp_budget.csv', index=False)
print(f'Generated {len(df)} rows')
print(df.head())