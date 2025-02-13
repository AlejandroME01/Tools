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

# Custom CSS for dark theme
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: #0e1117;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        color: #ffffff;
    }
    .stNumberInput > div > div > input {
        color: #ffffff;
    }
    .stSelectbox > div > div {
        background-color: #262730;
        color: #ffffff;
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

def calculate_greeks(r, S, K, T, sigma, type='C'):
    """Calculate option Greeks"""
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    if type == "C":
        delta = norm.cdf(d1)
        theta = (-S*sigma*norm.pdf(d1))/(2*np.sqrt(T)) - r*K*np.exp(-r*T)*norm.cdf(d2)
    else:
        delta = norm.cdf(d1) - 1
        theta = (-S*sigma*norm.pdf(d1))/(2*np.sqrt(T)) + r*K*np.exp(-r*T)*norm.cdf(-d2)
    
    gamma = norm.pdf(d1)/(S*sigma*np.sqrt(T))
    vega = S*np.sqrt(T)*norm.pdf(d1)
    
    return {
        'Delta': delta,
        'Gamma': gamma,
        'Theta': theta/365,  # Daily theta
        'Vega': vega/100    # Vega per 1% change in volatility
    }

# Parameters Input
with st.container():
    st.subheader("Option Parameters")
    st.markdown("---")
    
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

# Calculate option price and Greeks
option_type_short = "C" if option_type == "Call" else "P"
price = BS(r, S, K, T, sigma, type=option_type_short)
greeks = calculate_greeks(r, S, K, T, sigma, type=option_type_short)

# Display Results
col1, col2 = st.columns(2)

with col1:
    st.markdown("---")
    st.subheader("Option Price")
    if price is not None:
        st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background-color: #262730; border-radius: 5px;'>
                <h3 style='color: #ffffff;'>{option_type} Option Price: ${price:.2f}</h3>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Could not calculate option price. Please check your inputs.")

with col2:
    st.markdown("---")
    st.subheader("Greeks")
    st.markdown(f"""
        <div style='padding: 1rem; background-color: #262730; border-radius: 5px;'>
            <table style='width: 100%; color: #ffffff;'>
                <tr>
                    <td>Delta: {greeks['Delta']:.4f}</td>
                    <td>Gamma: {greeks['Gamma']:.4f}</td>
                    <td>Theta: {greeks['Theta']:.4f}</td>
                    <td>Vega: {greeks['Vega']:.4f}</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

# Sensitivity Analysis
st.markdown("---")
st.subheader("Sensitivity Analysis")

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
        line=dict(color='#00ff00', width=2)
    ))
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        hovermode='x',
        height=500,
        margin=dict(t=30, b=50, l=50, r=30),
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font=dict(color='#ffffff'),
        xaxis=dict(showgrid=True, gridcolor='#262730', gridwidth=1),
        yaxis=dict(showgrid=True, gridcolor='#262730', gridwidth=1)
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

