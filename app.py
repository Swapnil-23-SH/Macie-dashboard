import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="MACIE | Intelligence Console", page_icon="◈", layout="wide", initial_sidebar_state="expanded")

# Visual theme: deep navy, cyan accents, glass-like panels.
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --bg:#07111f; --panel:#0d1b2d; --panel2:#10243a; --line:#203b55; --cyan:#58e6f2; --blue:#6b8cff; --muted:#9cb3c9; --white:#eef7ff; }
html, body, [class*="css"] { font-family:'Manrope',sans-serif; }
.stApp { background: radial-gradient(ellipse at 15% 0%, #12314a 0%, #081321 42%, #050b14 100%); color:var(--white); }
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
[data-testid="stSidebar"] { background: linear-gradient(180deg,#0b1b2c 0%,#07111f 100%); border-right:1px solid #1e3a53; }
[data-testid="stSidebar"] * { color:#e8f5ff; }
.block-container { max-width:1500px; padding-top:1.7rem; padding-bottom:3rem; }
h1,h2,h3 { color:#f1f8ff !important; letter-spacing:-.035em; }
h1 { font-weight:800 !important; }
p, label, .stMarkdown { color:#d1e2f2; }
div[data-testid="stMetric"] { background:linear-gradient(135deg,rgba(18,42,65,.96),rgba(9,24,41,.96)); border:1px solid #23445e; padding:17px 18px; border-radius:16px; box-shadow:0 8px 28px rgba(0,0,0,.16); }
div[data-testid="stMetricLabel"] { color:#9cb8cf !important; font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; }
div[data-testid="stMetricValue"] { color:#f1fbff !important; font-weight:800; }
div[data-testid="stMetricDelta"] { color:#58e6f2 !important; }
.stTabs [data-baseweb="tab-list"] { gap:8px; background:#091827; border:1px solid #1c3850; border-radius:14px; padding:7px; }
.stTabs [data-baseweb="tab"] { border-radius:10px; color:#9fb7cd; padding:10px 16px; }
.stTabs [aria-selected="true"] { background:#173a53 !important; color:#66edf4 !important; }
.stButton>button { border-radius:10px; border:1px solid #3e738d; background:linear-gradient(135deg,#123b56,#135367); color:#effcff; }
div[data-testid="stAlert"] { background:#10263a; border:1px solid #27516a; color:#d9f7ff; border-radius:12px; }
hr { border-color:#203b55; }
div[data-testid="stDataFrame"] { border:1px solid #25445d; border-radius:12px; overflow:hidden; }
div[data-testid="stPlotlyChart"] { background:rgba(9,23,38,.72); border:1px solid #1e3b53; border-radius:16px; padding:8px; }
div[data-testid="stVerticalBlockBorderWrapper"] { border-color:#23445e !important; border-radius:16px !important; }
.smallcaps { color:#69eaf4; font-family:'DM Mono',monospace; text-transform:uppercase; letter-spacing:.16em; font-size:.72rem; }
.hero { padding:26px 28px; border:1px solid #24516a; border-radius:20px; background:linear-gradient(115deg,rgba(18,53,77,.9),rgba(9,22,38,.86)); box-shadow:0 14px 48px rgba(0,0,0,.22); position:relative; overflow:hidden; }
.hero:after { content:""; position:absolute; width:300px; height:300px; right:-90px; top:-140px; border-radius:50%; border:1px solid rgba(88,230,242,.25); box-shadow:0 0 0 25px rgba(88,230,242,.025),0 0 0 55px rgba(88,230,242,.025),0 0 55px rgba(88,230,242,.12); }
.hero-title { font-size:2.7rem; font-weight:800; letter-spacing:-.06em; line-height:1.05; color:#f3fbff; }
.hero-sub { color:#a9c4d8; font-size:1rem; margin-top:10px; max-width:700px; }
.pill { display:inline-block; border:1px solid #2f7184; border-radius:999px; padding:5px 10px; color:#6cebf2; background:rgba(47,113,132,.15); font: .72rem 'DM Mono',monospace; letter-spacing:.08em; }
.section-kicker { color:#64e5f0; font: .72rem 'DM Mono',monospace; text-transform:uppercase; letter-spacing:.14em; margin-bottom:5px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="smallcaps">MACIE</div>
  <div class="hero-title">See the stress.<br>Understand the signal.</div>
  <div class="hero-sub">A supply-chain-aware MSME financial assessment concept — turning cash-flow inputs into explainable early-warning signals and hypothetical funding scenarios.</div>
  
</div>
""", unsafe_allow_html=True)
st.write("")

with st.sidebar:
    st.markdown('<div class="smallcaps">01 / Business profile</div>', unsafe_allow_html=True)
    st.title("Input console")
    business_name = st.text_input("Business label", "Northstar Components · Demo")
    monthly_sales = st.number_input("Monthly inflows (₹)", min_value=0, max_value=100000000, value=500000, step=25000)
    monthly_costs = st.number_input("Monthly operating outflows (₹)", min_value=0, max_value=100000000, value=420000, step=25000)
    cash_buffer_days = st.slider("Cash buffer (days)", 0, 90, 12)
    delayed_receivables = st.number_input("Delayed receivables (₹)", min_value=0, max_value=100000000, value=150000, step=10000)
    delay_days = st.slider("Average payment delay (days)", 0, 120, 30)
    sales_change = st.slider("Recent sales change (%)", -50, 50, -15)
    debt_burden = st.slider("Debt repayments / sales (%)", 0, 80, 20)
    buyer_concentration = st.slider("Largest buyer share (%)", 0, 100, 55)
    supplier_dependency = st.slider("Largest supplier share (%)", 0, 100, 45)
    st.markdown("---")
    st.markdown('<div class="smallcaps">02 / Scenario lab</div>', unsafe_allow_html=True)
    invoice_finance = st.number_input("Invoice financing (₹)", 0, 100000000, 100000, step=10000)
    working_capital = st.number_input("Working-capital facility (₹)", 0, 100000000, 150000, step=10000)
    financing_cost_pct = st.slider("Illustrative funding cost (%)", 0, 20, 5)

daily_cost = monthly_costs / 30 if monthly_costs else 0
cash_buffer = daily_cost * cash_buffer_days
net_monthly = monthly_sales - monthly_costs
effective_inflows = monthly_sales * (1 + sales_change / 100)
estimated_position = cash_buffer + effective_inflows - monthly_costs - delayed_receivables
baseline_gap = max(0, -estimated_position)

points = 0
reasons = []
if net_monthly < 0: points += 2; reasons.append("Operating outflows exceed expected inflows.")
if estimated_position < 0: points += 2; reasons.append("Estimated cash position is negative before new funding.")
if delay_days >= 30: points += 1; reasons.append("Average payment delay is 30 days or more.")
if buyer_concentration >= 50: points += 1; reasons.append("Revenue is concentrated in one major buyer.")
if supplier_dependency >= 50: points += 1; reasons.append("Purchases are concentrated in one major supplier.")
if sales_change <= -10: points += 1; reasons.append("Recent sales have fallen by 10% or more.")
if debt_burden >= 35: points += 1; reasons.append("Debt repayments are a high share of sales.")
stress_label = "HIGH" if points >= 5 else "ELEVATED" if points >= 3 else "LOW"

def scenario_gap(funding):
    net_funding = max(0, funding * (1 - financing_cost_pct / 100))
    return max(0, -(estimated_position + net_funding))

invoice_gap = scenario_gap(invoice_finance)
wc_gap = scenario_gap(working_capital)

st.markdown(f'<div class="section-kicker">Live assessment / {business_name}</div>', unsafe_allow_html=True)
st.markdown("### Financial signal overview")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Monthly net cash", f"₹{net_monthly:,.0f}")
m2.metric("Estimated cash position", f"₹{estimated_position:,.0f}")
m3.metric("Potential cash gap", f"₹{baseline_gap:,.0f}")
m4.metric("Stress signal", stress_label, f"{points} rule points")

gauge_col, explain_col = st.columns([1, 1.45])
with gauge_col:
    st.markdown("#### Stress signal index")
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=points, number={"suffix": " / 9", "font": {"color": "#effbff", "size": 32}},
        title={"text": "Illustrative rule points", "font": {"color": "#9cb8cf", "size": 14}},
        gauge={"axis": {"range": [0, 9], "tickcolor": "#8ca9bf"},
               "bar": {"color": "#58e6f2"},
               "bgcolor": "#0d1b2d", "bordercolor": "#24475f",
               "steps": [{"range": [0, 3], "color": "#173c43"}, {"range": [3, 5], "color": "#3d3b2d"}, {"range": [5, 9], "color": "#4a2935"}]}
    ))
    fig.update_layout(height=250, margin=dict(l=20,r=20,t=45,b=10), paper_bgcolor="rgba(0,0,0,0)", font_color="#eef7ff")
    st.plotly_chart(fig, use_container_width=True)
with explain_col:
    st.markdown("#### Signal explanation")
    st.write("The indicator is driven by transparent demo rules—not a trained model or probability.")
    if reasons:
        for reason in reasons:
            st.markdown(f"- {reason}")
    else:
        st.success("No warning rules triggered for these example inputs.")
    st.caption("Change the controls in the left console to see how the illustrative signal responds.")

st.markdown("---")
tabs = st.tabs(["◈ Cash-flow lab", "⌘ Supply-chain map", "⇄ Funding scenarios", "↗ Roadmap"])

with tabs[0]:
    st.markdown('<div class="section-kicker">01 / Cash-flow lab</div>', unsafe_allow_html=True)
    st.subheader("Where pressure is building")
    a, b = st.columns([1.2, 1])
    with a:
        cash_df = pd.DataFrame({
            "Component": ["Cash buffer", "Adjusted inflows", "Operating outflows", "Delayed receivables"],
            "Amount (₹)": [cash_buffer, effective_inflows, -monthly_costs, -delayed_receivables]
        })
        fig = px.bar(cash_df, x="Component", y="Amount (₹)", color="Amount (₹)",
                     color_continuous_scale=["#ff6584", "#284b70", "#58e6f2"], title="Components of the simplified cash position")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#d9eaf8",
                          xaxis_title="", yaxis_title="₹ (illustrative)", coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with b:
        st.markdown("#### Profile telemetry")
        profile_df = pd.DataFrame({"Signal": ["Cash buffer", "Payment delay", "Largest buyer", "Largest supplier", "Debt / sales", "Sales change"],
                                   "Value": [f"{cash_buffer_days} days", f"{delay_days} days", f"{buyer_concentration}%", f"{supplier_dependency}%", f"{debt_burden}%", f"{sales_change}%"]})
        st.dataframe(profile_df, hide_index=True, use_container_width=True)
        st.caption("Inputs are illustrative and are not independently verified.")

with tabs[1]:
    st.markdown('<div class="section-kicker">02 / Relationship intelligence</div>', unsafe_allow_html=True)
    st.subheader("Supply-chain relationship map")
    st.caption("Conceptual network for the demo. Connections are not live and do not represent verified companies.")
    nodes = [("Supplier A",0,1),("Supplier B",0,-1),(business_name,1.5,0),("Buyer A",3,1),("Buyer B",3,-1),("Lender · concept",4.5,0)]
    edges = [("Supplier A",business_name,"Supplies"),("Supplier B",business_name,"Supplies"),(business_name,"Buyer A","Sells to"),(business_name,"Buyer B","Sells to"),(business_name,"Lender · concept","Potential financing")]
    node_df = pd.DataFrame(nodes, columns=["name","x","y"])
    pos = {r["name"]:(r["x"],r["y"]) for _,r in node_df.iterrows()}
    fig = go.Figure()
    for source,target,label in edges:
        x0,y0=pos[source]; x1,y1=pos[target]
        fig.add_trace(go.Scatter(x=[x0,x1],y=[y0,y1],mode="lines",line=dict(color="#35637d",width=2),hoverinfo="text",text=[label,label],showlegend=False))
    fig.add_trace(go.Scatter(x=node_df.x,y=node_df.y,mode="markers+text",text=node_df.name,textposition="bottom center",
                             marker=dict(size=27,color="#153f58",line=dict(color="#58e6f2",width=2)),
                             textfont=dict(color="#e7f7ff",size=12),hovertext=node_df.name,hoverinfo="text",showlegend=False))
    fig.update_layout(height=420, paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                      font_color="#d9eaf8",xaxis=dict(visible=False),yaxis=dict(visible=False),margin=dict(l=10,r=10,t=15,b=35))
    st.plotly_chart(fig,use_container_width=True)
    st.caption("The network illustrates intended relationship analysis; it is not a graph neural network.")

with tabs[2]:
    st.markdown('<div class="section-kicker">03 / Scenario lab</div>', unsafe_allow_html=True)
    st.subheader("What could funding change?")
    scenarios = pd.DataFrame({"Scenario":["No new facility","Invoice financing","Working-capital facility"],
                              "Remaining cash gap (₹)":[baseline_gap,invoice_gap,wc_gap]})
    fig = px.bar(scenarios,x="Scenario",y="Remaining cash gap (₹)",text=scenarios["Remaining cash gap (₹)"].map(lambda x: f"₹{x:,.0f}"),
                 color="Scenario",color_discrete_sequence=["#54708a","#58e6f2","#6b8cff"],title="Hypothetical remaining cash gap")
    max_gap = max(scenarios["Remaining cash gap (₹)"].max(), 10000)
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#d9eaf8",
                      xaxis_title="",yaxis_title="₹ (illustrative)",showlegend=False,
                      yaxis=dict(range=[0, max_gap * 1.25], rangemode="tozero", gridcolor="#203b55", zeroline=True),
                      margin=dict(t=65,b=20,l=10,r=10))
    st.plotly_chart(fig,use_container_width=True)
    if baseline_gap == 0:
        st.info("No cash gap is estimated with the current inputs. For a visible example, lower the cash buffer, increase delayed receivables, or set a more negative sales change in the left panel.")
    cols=st.columns(3)
    cols[0].metric("Baseline gap",f"₹{baseline_gap:,.0f}")
    cols[1].metric("Invoice finance gap",f"₹{invoice_gap:,.0f}",f"₹{max(0,baseline_gap-invoice_gap):,.0f} reduction")
    cols[2].metric("Working-capital gap",f"₹{wc_gap:,.0f}",f"₹{max(0,baseline_gap-wc_gap):,.0f} reduction")
    st.caption("Simplified arithmetic only. Eligibility, repayment schedules, collateral, interest timing, and actual cash-flow timing are not modelled.")

with tabs[3]:
    st.markdown('<div class="section-kicker">04 / Build roadmap</div>', unsafe_allow_html=True)
    st.subheader("From concept to validated decision support")
    r1,r2,r3 = st.columns(3)
    with r1:
        st.markdown("#### NOW")
        st.write("Interactive inputs")
        st.write("Transparent cash-gap arithmetic")
        st.write("Rule-based warning signal")
        st.write("Conceptual network and scenario lab")
    with r2:
        st.markdown("#### NEXT")
        st.write("Authorised, quality-checked data")
        st.write("Historical outcome validation")
        st.write("Measure false alarms and missed risks")
        st.write("Document uncertainty and limitations")
    with r3:
        st.markdown("#### LATER")
        st.write("Validated cash-flow forecasting")
        st.write("Temporal supply-chain analysis")
        st.write("Privacy safeguards")
        st.write("Carefully governed lender decision support")
    st.info("MACIE provides illustrative decision-support analysis and does not make lending decisions or claim validated real-world prediction accuracy.")

st.markdown("---")
st.markdown('<div class="smallcaps">MACIE • Explainable signals, responsible development</div>', unsafe_allow_html=True)
st.caption("Synthetic example data only. No confidential business or customer information should be entered.")
