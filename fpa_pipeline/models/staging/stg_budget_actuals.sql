with source as (
    select * from {{ source('meridian', 'raw_budget_actuals') }}
),

renamed as (
    select
        year,
        month,
        department,
        cost_category,
        budget,
        actuals,
        round(actuals - budget, 2) as variance_amount,
        round((actuals - budget) / nullif(budget, 0) * 100, 2) as variance_pct
    from source
)

select * from renamed
