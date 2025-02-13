import streamlit as st
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Black-Scholes Option Calculator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main > div {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Description
st.title("Black-Scholes Option Calculator")
st.markdown("---")
st.write("Calculate European Option Prices using the Black-Scholes Model")

def BS(r, S, K, T, sigma, type='C'):
    """Calculate BS option price for a Call or a Put"""
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try:
        if type == "C":
            price = S*norm.cdf(d1, 0, 1) - K*np.exp(-r*T)*norm.cdf(d2, 0, 1)
        elif type == "P":
            price = K*np.exp(-r*T)*norm.cdf(-d2, 0, 1) - S*norm.cdf(-d1, 0, 1)
        return price    
    except:
        return None

# Create container for input parameters
with st.container():
    st.subheader("Option Parameters")
    st.markdown("---")
    
    # Create three columns for better parameter organization
    col1, col2, col3 = st.columns(3)
    
    with col1:
        option_type = st.selectbox("Option Type", ["Call", "Put"])
        S = st.number_input("Current Stock Price (S)", 
                           min_value=0.01, 
                           value=30.0, 
                           step=0.1,
                           format="%.2f")
    
    with col2:
        K = st.number_input("Strike Price (K)", 
                           min_value=0.01, 
                           value=40.0, 
                           step=0.1,
                           format="%.2f")
        T = st.number_input("Time to Maturity (days)", 
                           min_value=1, 
                           value=240, 
                           step=1) / 365
    
    with col3:
        r = st.number_input("Risk-free Rate (r)", 
                           min_value=0.0, 
                           value=0.01, 
                           step=0.001, 
                           format="%.3f")
        sigma = st.number_input("Volatility (σ)", 
                               min_value=0.01, 
                               value=0.30, 
                               step=0.01,
                               format="%.2f")

# Calculate option price
option_type_short = "C" if option_type == "Call" else "P"
price = BS(r, S, K, T, sigma, type=option_type_short)

# Display the result in a container
with st.container():
    st.markdown("---")
    st.subheader("Option Price")
    if price is not None:
        st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background-color: #f0f2f6; border-radius: 5px;'>
                <h3>The {option_type} Option Price is: ${price:.2f}</h3>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Could not calculate option price. Please check your inputs.")

# Sensitivity Analysis
st.markdown("---")
st.subheader("Sensitivity Analysis")

# Create tabs for different sensitivity analyses
tab1, tab2, tab3 = st.tabs([
    "Stock Price Sensitivity",
    "Volatility Sensitivity",
    "Time Sensitivity"
])

def create_sensitivity_plot(x_values, y_values, title, x_label, y_label):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines',
        name='Option Price',
        line=dict(color='#1f77b4', width=2)
    ))
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        hovermode='x',
        height=500,
        margin=dict(t=30, b=50, l=50, r=30),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0')
    )
    return fig

with tab1:
    stock_prices = np.linspace(max(0.1, S-20), S+20, 100)
    prices = [BS(r, s, K, T, sigma, type=option_type_short) for s in stock_prices]
    fig = create_sensitivity_plot(
        stock_prices, prices,
        'Option Price vs Stock Price',
        'Stock Price ($)',
        'Option Price ($)'
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    vols = np.linspace(max(0.01, sigma-0.2), sigma+0.2, 100)
    prices = [BS(r, S, K, T, v, type=option_type_short) for v in vols]
    fig = create_sensitivity_plot(
        vols, prices,
        'Option Price vs Volatility',
        'Volatility (σ)',
        'Option Price ($)'
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    times = np.linspace(1/365, 2, 100)
    prices = [BS(r, S, K, t, sigma, type=option_type_short) for t in times]
    fig = create_sensitivity_plot(
        times*365, prices,
        'Option Price vs Time to Maturity',
        'Days to Maturity',
        'Option Price ($)'
    )
    st.plotly_chart(fig, use_container_width=True)


