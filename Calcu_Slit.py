import streamlit as st
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Black-Scholes Option Calculator", layout="wide")

st.title("Black-Scholes Option Calculator")
st.write("Calculate European Option Prices usinpipg the Black-Scholes Model")

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

# Create two columns for input parameters
col1, col2 = st.columns(2)

with col1:
    st.subheader("Option Parameters")
    option_type = st.selectbox("Option Type", ["Call", "Put"])
    S = st.number_input("Current Stock Price (S)", min_value=0.01, value=30.0, step=0.1)
    K = st.number_input("Strike Price (K)", min_value=0.01, value=40.0, step=0.1)
    
with col2:
    T = st.number_input("Time to Maturity (in days)", min_value=1, value=240, step=1) / 365
    r = st.number_input("Risk-free Rate (r)", min_value=0.0, value=0.01, step=0.001, format="%.3f")
    sigma = st.number_input("Volatility (σ)", min_value=0.01, value=0.30, step=0.01)

# Calculate option price
option_type_short = "C" if option_type == "Call" else "P"
price = BS(r, S, K, T, sigma, type=option_type_short)

# Display the result
st.subheader("Option Price")
if price is not None:
    st.write(f"The {option_type} Option Price is: ${price:.2f}")
else:
    st.error("Could not calculate option price. Please check your inputs.")

# Create sensitivity analysis
st.subheader("Sensitivity Analysis")

# Create tabs for different sensitivity analyses
tab1, tab2, tab3 = st.tabs(["Stock Price Sensitivity", "Volatility Sensitivity", "Time Sensitivity"])

with tab1:
    # Stock price sensitivity
    stock_prices = np.linspace(max(0.1, S-20), S+20, 100)
    prices = [BS(r, s, K, T, sigma, type=option_type_short) for s in stock_prices]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_prices, y=prices, mode='lines', name='Option Price'))
    fig.update_layout(
        title='Option Price vs Stock Price',
        xaxis_title='Stock Price',
        yaxis_title='Option Price',
        hovermode='x'
    )
    st.plotly_chart(fig)

with tab2:
    # Volatility sensitivity
    vols = np.linspace(max(0.01, sigma-0.2), sigma+0.2, 100)
    prices = [BS(r, S, K, T, v, type=option_type_short) for v in vols]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=vols, y=prices, mode='lines', name='Option Price'))
    fig.update_layout(
        title='Option Price vs Volatility',
        xaxis_title='Volatility',
        yaxis_title='Option Price',
        hovermode='x'
    )
    st.plotly_chart(fig)

with tab3:
    # Time sensitivity
    times = np.linspace(1/365, 2, 100)  # 1 day to 2 years
    prices = [BS(r, S, K, t, sigma, type=option_type_short) for t in times]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times*365, y=prices, mode='lines', name='Option Price'))
    fig.update_layout(
        title='Option Price vs Time to Maturity',
        xaxis_title='Days to Maturity',
        yaxis_title='Option Price',
        hovermode='x'
    )
    st.plotly_chart(fig)

# Add explanations
st.subheader("Model Parameters Explanation")
st.markdown("""
- **S**: Current stock price - The current price of the underlying asset
- **K**: Strike price - The price at which the option can be exercised
- **T**: Time to maturity - The time remaining until the option expires (in years)
- **r**: Risk-free rate - The theoretical rate of return of an investment with zero risk
- **σ (sigma)**: Volatility - A measure of the stock's price variability
""")

st.subheader("Assumptions of the Black-Scholes Model")
st.markdown("""
1. The option is European (can only be exercised at maturity)
2. No dividends are paid during the option's life
3. Markets are efficient (market movements cannot be predicted)
4. No transaction costs exist
5. The risk-free rate and volatility of the underlying are known and constant
6. The returns on the underlying are normally distributed
""")