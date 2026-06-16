import streamlit as st
import pandas as pd
import base64
import plotly.graph_objects as go

# --- Password Gate ---
st.markdown("## 🔒 Secure Access")

password = st.text_input("Enter access code:", type="password")

if password != "Bariatrics":
    st.warning("Please enter the correct access code to continue.")
    st.stop()
    
# Page config
st.set_page_config(page_title="Theatre Case Mix Simulation", layout="wide")

# Function to convert local image to base64
def get_base64_image(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_image("logo.png")  # make sure logo.png is in the same folder

# Top bar CSS
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(
                180deg,
                #f4f7ff 0%,
                #e4ecff 50%,
                #dce7ff 100%
            );
        }

        [data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }
        .top-bar {
            background-color: #1010EB;  /* Bright blue */
            padding: 10px 20px;
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        .top-bar h1 {
            color: white;
            font-size: 24px;
            margin: 0;
        }
        .top-bar .logo {
            height: 90px;
            margin-right: 5px;
        }
        .metric-card {
            background-color: #f9f9ff;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            text-align: center;
            margin: 5px;
            min-height: 130px;
        }
        .metric-card h3 {
            margin: 0;
            font-size: 18px;
            color: #333333;
        }
        .metric-card p {
            margin: 5px 0 0;
            font-size: 24px;
            font-weight: bold;
            color: #1010EB;
        }
        .metric-card span {
            font-size: 13px;
            color: #666666;
        }
        .good { color: #2ca02c !important; }
        .warn { color: #d62728 !important; }
        .revenue-box {
            background-color: #eafbea;
            border-left: 5px solid #2ca02c;
            padding: 28px;
            border-radius: 20px;
            font-size: 16px;
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)

# Display logo
st.markdown(f"""
    <div class="top-bar">
        <img src="data:image/png;base64,{logo_base64}" class="logo" alt="Company Logo">
    </div>
""", unsafe_allow_html=True)

st.title("Theatre Case Mix Simulation")

# Procedure data
# Revenue is based on the value attached to each procedure and can be amended here.
procedures_data = [
    {"name": "Hernia", "points": 1.3, "time": 80, "risk_points": 0.25, "complex_points": 0.5, "revenue": 2529},
    {"name": "Lap Cholecystectomy", "points": 1.6, "time": 96, "risk_points": 0.25, "complex_points": 0.5, "revenue": 4099},
    {"name": "Sleeve Gastrectomy", "points": 2, "time": 120, "risk_points": 0.25, "complex_points": 0.5, "revenue": 6683},
    {"name": "Gastric Bypass", "points": 2.5, "time": 150, "risk_points": 0.25, "complex_points": 0.5, "revenue": 9180},
    {"name": "Revision Surgery/Complex", "points": 4, "time": 210, "risk_points": 0.25, "complex_points": 0.5, "revenue": 10232},
]

df_procedures = pd.DataFrame(procedures_data)
st.subheader("Procedures Overview")

# Ensure numeric columns are float
df_procedures['points'] = df_procedures['points'].astype(float)
df_procedures['risk_points'] = df_procedures['risk_points'].astype(float)
df_procedures['complex_points'] = df_procedures['complex_points'].astype(float)
df_procedures['time'] = df_procedures['time'].astype(float)
df_procedures['revenue'] = df_procedures['revenue'].astype(float)

clean_df = df_procedures[['name', 'time', 'points', 'risk_points', 'complex_points', 'revenue']].rename(columns={
    'name': 'Procedure',
    'time': 'Time (minutes)',
    'points': 'Base Points',
    'risk_points': 'Risk Points',
    'complex_points': 'Complex Points',
    'revenue': 'Revenue per Case'
})

# Format values for display only
display_df = clean_df.copy()
display_df['Time (minutes)'] = display_df['Time (minutes)'].map(lambda x: f"{x:.0f}")
display_df['Base Points'] = display_df['Base Points'].map(lambda x: f"{x:.1f}")
display_df['Risk Points'] = display_df['Risk Points'].map(lambda x: f"{x:.2f}")
display_df['Complex Points'] = display_df['Complex Points'].map(lambda x: f"{x:.2f}")
display_df['Revenue per Case'] = display_df['Revenue per Case'].map(lambda x: f"£{x:,.2f}")

# Build HTML table
html = """
<table style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif;">
<tr>
"""
# Table headers with background
for col in display_df.columns:
    html += f'<th style="background-color: #f0f8ff; color: #1010EB; font-size: 20px; font-weight:bold; text-align:center; padding:8px;">{col}</th>'
html += "</tr>"

# Table rows
for _, row in display_df.iterrows():
    html += "<tr>"
    for i, col in enumerate(display_df.columns):
        if i == 0 or i == 2 or i == 5:  # procedure, base points and revenue bold
            html += f'<td style="{"background-color: #f0f8ff;" if i==0 else ""} font-weight:bold; text-align:center; padding:6px;">{row[col]}</td>'
        else:
            html += f'<td style="text-align:center; padding:6px;">{row[col]}</td>'
    html += "</tr>"

html += "</table>"

# Display HTML table
st.markdown(html, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Center the input visually
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style="
        background-color: #f0f4ff;
        padding: 20px 24px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        font-family: Arial, sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
    ">
        <label style="
            font-weight:bold;
            font-size:16px;
            margin-bottom:0;
        ">
            Available Theatre Time (minutes)
        </label>
    """, unsafe_allow_html=True)

    available_time = st.number_input(
        "",
        min_value=0,
        value=510,
        step=5,
        key="available_time_styled"
    )

    st.markdown("</div>", unsafe_allow_html=True)

# Case selection
st.subheader("Select Cases")
total_points = 0
total_time = 0
total_cases = 0
total_revenue = 0
case_details = []

for proc in procedures_data:
    num_cases = st.number_input(
        f"{proc['name']} - Cases",
        min_value=0,
        value=0,
        step=1,
        key=f"{proc['name']}_count"
    )

    for i in range(num_cases):
        # Compact row: label + toggles
        col_label, col_risk, col_complex = st.columns([3, 1, 1])
        with col_label:
            st.write(f"Case {i+1}")
        with col_risk:
            add_risk = st.checkbox("⚠️ High Risk", key=f"{proc['name']}_{i}_risk")
        with col_complex:
            add_complex = st.checkbox("➕ Extra Complex", key=f"{proc['name']}_{i}_complex")

        case_points = proc["points"]
        case_time = proc["time"]
        case_revenue = proc["revenue"]

        if add_risk:
            case_points += proc["risk_points"]
            case_time += 15
        if add_complex:
            case_points += proc["complex_points"]
            case_time += 30

        total_cases += 1
        total_points += case_points
        total_time += case_time
        total_revenue += case_revenue

        case_details.append({
            "procedure": proc["name"],
            "case_number": i+1,
            "points": case_points,
            "time": case_time,
            "high_risk": add_risk,
            "extra_complex": add_complex,
            "revenue": case_revenue
        })

utilisation = (total_time / available_time) * 100 if available_time else 0
baseline_utilisation = 70
target_utilisation = 85
revenue_per_hour = 1803.4

utilisation_revenue = 0
if utilisation > baseline_utilisation:
    extra_minutes = total_time - (available_time * baseline_utilisation / 100)
    utilisation_revenue = (extra_minutes / 60) * revenue_per_hour

# Baseline revenue logic:
# Baseline assumes 3 cases per list, aiming for 2 general surgery cases and 1 bariatric case if available.
def select_baseline_cases(cases):
    general_cases = []
    bariatric_cases = []

    for case in cases:
        name = case["procedure"]
        if "Hernia" in name or "Lap Chole" in name:
            if len(general_cases) < 2:
                general_cases.append(case)
        elif "Sleeve" in name or "Bypass" in name or "Revision" in name:
            if len(bariatric_cases) < 1:
                bariatric_cases.append(case)

    baseline_cases = general_cases + bariatric_cases

    # Fill remaining baseline slots, if fewer than 3, with earliest remaining selected cases.
    if len(baseline_cases) < 3:
        used_ids = set(id(c) for c in baseline_cases)
        remaining = [c for c in cases if id(c) not in used_ids]
        baseline_cases += remaining[:3 - len(baseline_cases)]

    return baseline_cases[:3]

baseline_cases = select_baseline_cases(case_details)
current_revenue = sum(case["revenue"] for case in baseline_cases)
extra_case_revenue = total_revenue - current_revenue
total_revenue_with_utilisation = total_revenue + utilisation_revenue
total_additional_revenue = total_revenue_with_utilisation - current_revenue

st.divider()

# --- Simulation Summary (Styled) ---
st.subheader("Simulation Summary")

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.markdown(f"""
        <div class="metric-card">
            <h3>Total Cases</h3>
            <p>{total_cases}</p>
            <span>All selected</span>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class="metric-card">
            <h3>Total Points</h3>
            <p>{total_points:.2f}</p>
            <span>Workload score</span>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
        <div class="metric-card">
            <h3>Total Time Used</h3>
            <p>{total_time} min</p>
            <span>Theatre time</span>
        </div>
    """, unsafe_allow_html=True)
with col4:
    utilisation_class = "good" if utilisation >= target_utilisation else "warn"
    st.markdown(f"""
        <div class="metric-card">
            <h3>Utilisation</h3>
            <p class="{utilisation_class}">{utilisation:.1f}%</p>
            <span>Target ≥ {target_utilisation}%</span>
        </div>
    """, unsafe_allow_html=True)
with col5:
    st.markdown(f"""
        <div class="metric-card">
            <h3>Total Revenue</h3>
            <p class="good">£{total_revenue_with_utilisation:,.0f}</p>
            <span>Procedures + utilisation</span>
        </div>
    """, unsafe_allow_html=True)
with col6:
    st.markdown(f"""
        <div class="metric-card">
            <h3>Additional Revenue</h3>
            <p class="good">£{total_additional_revenue:,.0f}</p>
            <span>vs baseline</span>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Annual projections
lists_per_year = 60
annual_baseline_cases = 3 * lists_per_year
annual_total_cases = total_cases * lists_per_year

annual_current_revenue = current_revenue * lists_per_year
annual_total_revenue = total_revenue_with_utilisation * lists_per_year
annual_additional_revenue = annual_total_revenue - annual_current_revenue
annual_extra_cases = annual_total_cases - annual_baseline_cases

# Revenue chart
labels = ["Annual Baseline\n(3 cases per list)", "Annual Improved Scenario\n(All selected cases + utilisation)"]
values_revenue = [annual_current_revenue, annual_total_revenue]

bar_text = [
    f"£{annual_current_revenue:,.0f}<br><sub>{annual_baseline_cases:,} cases/year</sub>",
    f"£{annual_total_revenue:,.0f}<br><sub>{annual_total_cases:,} cases/year</sub>"
]

fig = go.Figure()
fig.add_trace(go.Bar(
    x=labels,
    y=values_revenue,
    text=bar_text,
    textposition='auto',
    marker_color=['#1010EB', '#2ca02c'],
    name="Annual Revenue"
))

fig.add_annotation(
    x=0.5,
    y=max(values_revenue) * 0.95 if max(values_revenue) > 0 else 1,
    xref='paper',
    yref='y',
    text=f"+ £{annual_additional_revenue:,.0f}<br><sub>+{annual_extra_cases:,} cases/year</sub>",
    showarrow=True,
    arrowhead=3,
    arrowcolor='green',
    font=dict(color='green', size=16),
    ax=0,
    ay=40
)

fig.update_layout(
    title_text="Annual Revenue Comparison",
    xaxis_title="Scenario",
    yaxis_title="Amount (£)",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    barmode='group',
    font=dict(size=14)
)

# Case volume chart
fig_cases = go.Figure()
fig_cases.add_trace(go.Bar(
    x=["Annual Baseline\n(3 cases per list)", "Annual Improved Scenario\n(All selected cases)"],
    y=[annual_baseline_cases, annual_total_cases],
    text=[f"{annual_baseline_cases:,} cases", f"{annual_total_cases:,} cases"],
    textposition='auto',
    marker_color=['#1010EB', '#2ca02c'],
    name="Annual Cases"
))

fig_cases.add_annotation(
    x=0.5,
    y=max(annual_baseline_cases, annual_total_cases) * 0.95 if max(annual_baseline_cases, annual_total_cases) > 0 else 1,
    xref='paper',
    yref='y',
    text=f"+{annual_extra_cases:,} cases/year",
    showarrow=True,
    arrowhead=3,
    arrowcolor='green',
    font=dict(color='green', size=16),
    ax=0,
    ay=40
)

fig_cases.update_layout(
    title_text="Annual Case Volume Comparison",
    xaxis_title="Scenario",
    yaxis_title="Number of Cases",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(size=14)
)

col_chart, col_breakdown = st.columns([2, 1])

with col_chart:
    st.subheader("Annual Revenue Comparison Chart")
    st.markdown("<p style='font-size: 13px; color: #1f77b4;'>Based on 60 Bariatrics & General Surgery lists performed annually</p>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Annual Case Volume Chart")
    st.plotly_chart(fig_cases, use_container_width=True)

with col_breakdown:
    st.subheader("Additional Revenue Breakdown")

    st.markdown(f"""
    <div class="revenue-box">
        <p><strong>Baseline Revenue:</strong><br>£{current_revenue:,.2f}</p>
        <p><strong>Revenue from Additional Procedures:</strong><br>£{extra_case_revenue:,.2f}</p>
        <p><strong>Additional Revenue from Utilisation:</strong><br>£{utilisation_revenue:,.2f}</p>
        <p style='font-size: 12px; color: #555; margin-top: -10px;'>Only applies when utilisation exceeds current median ({baseline_utilisation}%)</p>
        <hr style="border-color:#2ca02c; margin: 10px 0;">
        <p><strong>Total Additional Revenue:</strong><br>£{total_additional_revenue:,.2f}</p>
        <p><strong>Total Revenue incl. Utilisation:</strong><br>£{total_revenue_with_utilisation:,.2f}</p>
    </div>
    """, unsafe_allow_html=True)

# Case breakdown (table view per procedure)
with st.expander("Case Breakdown"):
    grouped = {}
    for detail in case_details:
        proc = detail["procedure"]
        if proc not in grouped:
            grouped[proc] = []
        grouped[proc].append(detail)

    for proc, cases in grouped.items():
        st.markdown(f"### {proc}")
        proc_df = pd.DataFrame([{
            "Case": case["case_number"],
            "Points": case["points"],
            "Time (min)": case["time"],
            "Revenue": f"£{case['revenue']:,.2f}",
            "High Risk": "⚠️ Yes" if case["high_risk"] else "No",
            "Extra Complex": "➕ Yes" if case["extra_complex"] else "No"
        } for case in cases])
        st.dataframe(proc_df, hide_index=True, use_container_width=True)
