import streamlit as st

# Page config for mobile responsiveness
st.set_page_config(
    page_title="Task Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-friendly design
st.markdown("""
    <style>
    /* Mobile responsive adjustments */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 0.5rem;
        }
        h1 {
            font-size: 1.5rem !important;
        }
        h3 {
            font-size: 1.1rem !important;
        }
    }
    
    /* Card styling */
    .task-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 4px solid;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .in-progress {
        border-left-color: #3498db;
    }
    
    .delayed {
        border-left-color: #e74c3c;
    }
    
    .completed {
        border-left-color: #2ecc71;
    }
    
    .task-title {
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 8px;
        color: #2c3e50;
    }
    
    .task-meta {
        font-size: 0.85rem;
        color: #7f8c8d;
        margin-bottom: 5px;
    }
    
    .task-description {
        font-size: 0.9rem;
        color: #34495e;
        line-height: 1.4;
    }
    
    /* Column headers */
    .column-header {
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 15px;
        color: white;
        font-weight: 600;
    }
    
    .header-progress {
        background-color: #3498db;
    }
    
    .header-delayed {
        background-color: #e74c3c;
    }
    
    .header-completed {
        background-color: #2ecc71;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 5px;
    }
    
    .badge-high {
        background-color: #fee;
        color: #c33;
    }
    
    .badge-medium {
        background-color: #fff3cd;
        color: #856404;
    }
    
    .badge-low {
        background-color: #d1ecf1;
        color: #0c5460;
    }
    </style>
""", unsafe_allow_html=True)

# Dummy data
in_progress_tasks = [
    {
        "title": "Website Redesign",
        "assigned": "Sarah Johnson",
        "due": "Dec 15, 2025",
        "priority": "High",
        "description": "Complete homepage and navigation redesign with new branding"
    },
    {
        "title": "API Integration",
        "assigned": "Mike Chen",
        "due": "Nov 30, 2025",
        "priority": "Medium",
        "description": "Integrate third-party payment gateway API"
    },
    {
        "title": "User Testing Phase 2",
        "assigned": "Emily Davis",
        "due": "Nov 25, 2025",
        "priority": "Low",
        "description": "Conduct user testing sessions for mobile app features"
    }
]

delayed_tasks = [
    {
        "title": "Database Migration",
        "assigned": "John Smith",
        "due": "Oct 20, 2025",
        "priority": "High",
        "description": "Migrate legacy database to new cloud infrastructure"
    },
    {
        "title": "Security Audit",
        "assigned": "Lisa Wang",
        "due": "Oct 18, 2025",
        "priority": "High",
        "description": "Complete security vulnerability assessment and patch critical issues"
    }
]

completed_tasks = [
    {
        "title": "Mobile App Launch",
        "assigned": "Team Alpha",
        "completed": "Oct 22, 2025",
        "priority": "High",
        "description": "Successfully launched mobile app on iOS and Android platforms"
    },
    {
        "title": "Q3 Reports",
        "assigned": "Finance Team",
        "completed": "Oct 20, 2025",
        "priority": "Medium",
        "description": "Prepared and submitted quarterly financial reports"
    },
    {
        "title": "Client Presentation",
        "assigned": "Rachel Green",
        "completed": "Oct 19, 2025",
        "priority": "Medium",
        "description": "Delivered product demo presentation to key stakeholders"
    },
    {
        "title": "Documentation Update",
        "assigned": "Dev Team",
        "completed": "Oct 15, 2025",
        "priority": "Low",
        "description": "Updated technical documentation for API v2.0"
    }
]

# Header
st.title("📊 Task Dashboard")
st.markdown("---")

# Create three columns
col1, col2, col3 = st.columns(3)

# Column 1: In Progress
with col1:
    st.markdown(f"""
        <div class="column-header header-progress">
            🔄 IN PROGRESS ({len(in_progress_tasks)})
        </div>
    """, unsafe_allow_html=True)
    
    for task in in_progress_tasks:
        priority_class = f"badge-{task['priority'].lower()}"
        st.markdown(f"""
            <div class="task-card in-progress">
                <div class="task-title">{task['title']}</div>
                <div class="task-meta">👤 {task['assigned']}</div>
                <div class="task-meta">📅 Due: {task['due']}</div>
                <div class="task-description">{task['description']}</div>
                <span class="badge {priority_class}">{task['priority']} Priority</span>
            </div>
        """, unsafe_allow_html=True)

# Column 2: Delayed
with col2:
    st.markdown(f"""
        <div class="column-header header-delayed">
            ⚠️ DELAYED ({len(delayed_tasks)})
        </div>
    """, unsafe_allow_html=True)
    
    for task in delayed_tasks:
        priority_class = f"badge-{task['priority'].lower()}"
        st.markdown(f"""
            <div class="task-card delayed">
                <div class="task-title">{task['title']}</div>
                <div class="task-meta">👤 {task['assigned']}</div>
                <div class="task-meta">📅 Was due: {task['due']}</div>
                <div class="task-description">{task['description']}</div>
                <span class="badge {priority_class}">{task['priority']} Priority</span>
            </div>
        """, unsafe_allow_html=True)

# Column 3: Completed
with col3:
    st.markdown(f"""
        <div class="column-header header-completed">
            ✅ COMPLETED ({len(completed_tasks)})
        </div>
    """, unsafe_allow_html=True)
    
    for task in completed_tasks:
        priority_class = f"badge-{task['priority'].lower()}"
        st.markdown(f"""
            <div class="task-card completed">
                <div class="task-title">{task['title']}</div>
                <div class="task-meta">👤 {task['assigned']}</div>
                <div class="task-meta">✓ Completed: {task['completed']}</div>
                <div class="task-description">{task['description']}</div>
                <span class="badge {priority_class}">{task['priority']} Priority</span>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; font-size: 0.9rem; padding: 20px;'>
        Dashboard last updated: October 26, 2025
    </div>
""", unsafe_allow_html=True)
