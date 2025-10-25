import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# Page config for mobile optimization
st.set_page_config(
    page_title="Employee Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile responsiveness
st.markdown("""
    <style>
    /* Mobile-friendly adjustments */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }
        h1 {
            font-size: 1.5rem;
        }
        h2 {
            font-size: 1.2rem;
        }
        h3 {
            font-size: 1rem;
        }
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    
    .employee-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Generate dummy employee data
@st.cache_data
def generate_employee_data():
    departments = ["Engineering", "Marketing", "Sales", "HR", "Finance", "Operations"]
    positions = ["Manager", "Senior", "Junior", "Lead", "Analyst", "Coordinator"]
    statuses = ["Active", "Active", "Active", "On Leave", "Remote"]
    
    employees = []
    for i in range(1, 26):
        emp = {
            "ID": f"EMP{i:03d}",
            "Name": f"{random.choice(['John', 'Jane', 'Mike', 'Sarah', 'David', 'Emily', 'Chris', 'Lisa', 'Tom', 'Anna'])} {random.choice(['Smith', 'Johnson', 'Brown', 'Davis', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson'])}",
            "Department": random.choice(departments),
            "Position": random.choice(positions),
            "Status": random.choice(statuses),
            "Salary": random.randint(40000, 120000),
            "Join Date": (datetime.now() - timedelta(days=random.randint(30, 1825))).strftime("%Y-%m-%d"),
            "Performance": random.randint(65, 100)
        }
        employees.append(emp)
    
    return pd.DataFrame(employees)

# Load data
df = generate_employee_data()

# Header
st.title("👥 Employee Dashboard")
st.markdown("---")

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Employees", len(df), "+2")
with col2:
    st.metric("Departments", df["Department"].nunique())
with col3:
    active = len(df[df["Status"] == "Active"])
    st.metric("Active", active)
with col4:
    avg_perf = df["Performance"].mean()
    st.metric("Avg Performance", f"{avg_perf:.1f}%")

st.markdown("---")

# Filters in expander for mobile
with st.expander("🔍 Filters", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        dept_filter = st.multiselect("Department", options=df["Department"].unique(), default=df["Department"].unique())
    with col2:
        status_filter = st.multiselect("Status", options=df["Status"].unique(), default=df["Status"].unique())

# Filter data
filtered_df = df[
    (df["Department"].isin(dept_filter)) & 
    (df["Status"].isin(status_filter))
]

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["📊 Overview", "👤 Employee List", "📈 Analytics"])

with tab1:
    # Department Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Department Distribution")
        dept_counts = filtered_df["Department"].value_counts()
        fig1 = px.pie(values=dept_counts.values, names=dept_counts.index, 
                      color_discrete_sequence=px.colors.qualitative.Set3)
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        fig1.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Status Overview")
        status_counts = filtered_df["Status"].value_counts()
        fig2 = px.bar(x=status_counts.index, y=status_counts.values,
                      color=status_counts.index,
                      color_discrete_sequence=px.colors.qualitative.Pastel)
        fig2.update_layout(showlegend=False, height=300, 
                          xaxis_title="", yaxis_title="Count",
                          margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig2, use_container_width=True)
    
    # Average Salary by Department
    st.subheader("Average Salary by Department")
    avg_salary = filtered_df.groupby("Department")["Salary"].mean().sort_values(ascending=True)
    fig3 = px.bar(x=avg_salary.values, y=avg_salary.index, orientation='h',
                  color=avg_salary.values,
                  color_continuous_scale='viridis')
    fig3.update_layout(height=400, xaxis_title="Average Salary ($)", yaxis_title="",
                      margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.subheader(f"Employee List ({len(filtered_df)} employees)")
    
    # Search box
    search = st.text_input("🔍 Search by name or ID", "")
    
    if search:
        search_df = filtered_df[
            filtered_df["Name"].str.contains(search, case=False) | 
            filtered_df["ID"].str.contains(search, case=False)
        ]
    else:
        search_df = filtered_df
    
    # Display employees as cards on mobile, table on desktop
    if st.checkbox("Card View (Mobile-friendly)", value=True):
        for _, emp in search_df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="employee-card">
                    <h3>{emp['Name']} <span style="color: #888; font-size: 0.9rem;">({emp['ID']})</span></h3>
                    <p><strong>Department:</strong> {emp['Department']} | <strong>Position:</strong> {emp['Position']}</p>
                    <p><strong>Status:</strong> {emp['Status']} | <strong>Performance:</strong> {emp['Performance']}%</p>
                    <p><strong>Salary:</strong> ${emp['Salary']:,} | <strong>Joined:</strong> {emp['Join Date']}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.dataframe(
            search_df[["ID", "Name", "Department", "Position", "Status", "Salary", "Performance"]],
            use_container_width=True,
            hide_index=True
        )

with tab3:
    st.subheader("Performance Analytics")
    
    # Performance distribution
    col1, col2 = st.columns(2)
    
    with col1:
        fig4 = px.histogram(filtered_df, x="Performance", nbins=20,
                           color_discrete_sequence=['#667eea'])
        fig4.update_layout(height=300, xaxis_title="Performance Score", yaxis_title="Count",
                          margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        # Performance by department
        perf_dept = filtered_df.groupby("Department")["Performance"].mean().sort_values(ascending=False)
        fig5 = px.bar(x=perf_dept.index, y=perf_dept.values,
                     color=perf_dept.values,
                     color_continuous_scale='RdYlGn')
        fig5.update_layout(height=300, xaxis_title="", yaxis_title="Avg Performance",
                          margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig5, use_container_width=True)
    
    # Salary vs Performance scatter
    st.subheader("Salary vs Performance Analysis")
    fig6 = px.scatter(filtered_df, x="Salary", y="Performance", 
                     color="Department", size="Performance",
                     hover_data=["Name", "Position"])
    fig6.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig6, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("*Dashboard last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M") + "*")
