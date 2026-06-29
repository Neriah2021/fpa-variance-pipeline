# Create sources.yml
sources = """version: 2

sources:
  - name: meridian
    database: project-3887205e-dca0-460f-b5b
    schema: Meridian_Corp
    tables:
      - name: raw_budget_actuals
"""
open('models/staging/sources.yml', 'w').write(sources)

# Fix staging model
f = open('models/staging/stg_budget_actuals.sql', 'w')
f.write('with source as (\n')
f.write("    select * from {{ source('meridian', 'raw_budget_actuals') }}\n")
f.write('),\n\n')
f.write('renamed as (\n')
f.write('    select\n')
f.write('        year,\n')
f.write('        month,\n')
f.write('        department,\n')
f.write('        cost_category,\n')
f.write('        budget,\n')
f.write('        actuals,\n')
f.write('        round(actuals - budget, 2) as variance_amount,\n')
f.write('        round((actuals - budget) / nullif(budget, 0) * 100, 2) as variance_pct\n')
f.write('    from source\n')
f.write(')\n\n')
f.write('select * from renamed\n')
f.close()
print('Done')