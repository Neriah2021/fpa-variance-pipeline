with staged as (
    select * from {{ ref('stg_budget_actuals') }}
),

aggregated as (
    select
        year,
        month,
        department,
        sum(budget) as total_budget,
        sum(actuals) as total_actuals,
        sum(variance_amount) as total_variance,
        round(sum(actuals - budget) / nullif(sum(budget), 0) * 100, 2) as variance_pct
    from staged
    group by year, month, department
)

select * from aggregated
