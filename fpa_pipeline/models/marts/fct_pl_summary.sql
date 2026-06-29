with dept_monthly as (
    select * from {{ ref('int_dept_monthly') }}
),

final as (
    select
        year,
        month,
        department,
        total_budget,
        total_actuals,
        total_variance,
        variance_pct,
        case
            when variance_pct > 10 then 'Over Budget'
            when variance_pct < -10 then 'Under Budget'
            else 'On Track'
        end as budget_status
    from dept_monthly
)

select * from final
order by year, month, department
