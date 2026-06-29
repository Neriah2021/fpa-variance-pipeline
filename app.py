import streamlit as st
import pandas as pd
from google.cloud import bigquery
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Meridian Corp FPA Dashboard', layout='wide')
st.title('Meridian Corp — FPA Variance Dashboard')
st.markdown('Budget vs Actuals analysis powered by BigQuery and dbt')
st.divider()

@st.cache_data
def load_data():
    client = bigquery.Client(project='project-3887205e-dca0-460f-b5b')
    query = """
        SELECT * FROM `project-3887205e-dca0-460f-b5b.Meridian_Corp.fct_pl_summary`
        ORDER BY year, month, department
    """
    return client.query(query).to_dataframe()

df = load_data()

# ── Filters ─────────────────────────────────────────────────
col_f1, col_f2 = st.columns(2)
with col_f1:
    year = st.selectbox('Year', sorted(df['year'].unique()), index=2)
with col_f2:
    dept = st.multiselect('Department', df['department'].unique(), default=list(df['department'].unique()))

filtered = df[(df['year'] == year) & (df['department'].isin(dept))]

# ── KPI Cards ───────────────────────────────────────────────
total_budget = filtered['total_budget'].sum()
total_actuals = filtered['total_actuals'].sum()
total_variance = filtered['total_variance'].sum()
over_budget = len(filtered[filtered['budget_status'] == 'Over Budget'])

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric('Total Budget', f'${total_budget/1e6:.1f}M')
with col2:
    st.metric('Total Actuals', f'${total_actuals/1e6:.1f}M')
with col3:
    st.metric('Total Variance', f'${total_variance/1e6:.1f}M')
with col4:
    st.metric('Over Budget Items', over_budget)

st.divider()

# ── Charts ───────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader('Budget vs Actuals by Department')
    dept_summary = filtered.groupby('department').agg(
        total_budget=('total_budget', 'sum'),
        total_actuals=('total_actuals', 'sum')
    ).reset_index()
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name='Budget', x=dept_summary['department'], y=dept_summary['total_budget'], marker_color='#0078D4'))
    fig1.add_trace(go.Bar(name='Actuals', x=dept_summary['department'], y=dept_summary['total_actuals'], marker_color='#00B294'))
    fig1.update_layout(barmode='group', xaxis_title='Department', yaxis_title='Amount ($)')
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader('Variance % by Department')
    dept_var = filtered.groupby('department').agg(
        total_budget=('total_budget', 'sum'),
        total_actuals=('total_actuals', 'sum')
    ).reset_index()
    dept_var['variance_pct'] = ((dept_var['total_actuals'] - dept_var['total_budget']) / dept_var['total_budget'] * 100).round(2)
    colors = ['#C00000' if x > 10 else '#00B294' if x < -10 else '#0078D4' for x in dept_var['variance_pct']]
    fig2 = go.Figure(go.Bar(x=dept_var['department'], y=dept_var['variance_pct'], marker_color=colors))
    fig2.add_hline(y=10, line_dash='dash', line_color='red', annotation_text='10% threshold')
    fig2.add_hline(y=-10, line_dash='dash', line_color='orange', annotation_text='-10% threshold')
    fig2.update_layout(xaxis_title='Department', yaxis_title='Variance %')
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Monthly trend ────────────────────────────────────────────
st.subheader('Monthly Variance Trend')
monthly = filtered.groupby('month').agg(
    total_budget=('total_budget', 'sum'),
    total_actuals=('total_actuals', 'sum')
).reset_index()
monthly['variance_pct'] = ((monthly['total_actuals'] - monthly['total_budget']) / monthly['total_budget'] * 100).round(2)
fig3 = px.line(monthly, x='month', y='variance_pct', markers=True, color_discrete_sequence=['#0078D4'])
fig3.add_hline(y=10, line_dash='dash', line_color='red')
fig3.add_hline(y=-10, line_dash='dash', line_color='orange')
fig3.update_layout(xaxis_title='Month', yaxis_title='Variance %')
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ── Flagged items table ──────────────────────────────────────
st.subheader('Flagged Items')
flagged = filtered[filtered['budget_status'] != 'On Track'].copy()
flagged['total_budget'] = flagged['total_budget'].apply(lambda x: f'${x:,.0f}')
flagged['total_actuals'] = flagged['total_actuals'].apply(lambda x: f'${x:,.0f}')
flagged['total_variance'] = flagged['total_variance'].apply(lambda x: f'${x:,.0f}')
flagged['variance_pct'] = flagged['variance_pct'].apply(lambda x: f'{x:.1f}%')
st.dataframe(flagged[['year', 'month', 'department', 'total_budget', 'total_actuals', 'total_variance', 'variance_pct', 'budget_status']], use_container_width=True, hide_index=True)