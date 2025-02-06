# Black-Scholes Option Calculator

A web-based calculator for European options using the Black-Scholes model, built with Streamlit. This application provides an intuitive interface for calculating option prices and visualizing various sensitivity analyses.

## Live Demo
Access the calculator at: [Your Streamlit Cloud URL]

## Features

- Calculate European Call and Put option prices
- Interactive parameter inputs:
  - Stock Price (S)
  - Strike Price (K)
  - Time to Maturity (T)
  - Risk-free Rate (r)
  - Volatility (σ)
- Visual sensitivity analysis:
  - Stock Price sensitivity
  - Volatility sensitivity
  - Time sensitivity
- Educational components explaining parameters and model assumptions

## Installation

To run this application locally:

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run calcu_slit.py
```

## Dependencies

- streamlit
- numpy
- scipy
- plotly
- pandas

All dependencies are listed in `requirements.txt`

## Black-Scholes Model

The Black-Scholes model is used to calculate the theoretical price of European-style options. The model assumes:

1. The option is European (can only be exercised at maturity)
2. No dividends are paid during the option's life
3. Markets are efficient (market movements cannot be predicted)
4. No transaction costs exist
5. The risk-free rate and volatility of the underlying are known and constant
6. The returns on the underlying are normally distributed

## Usage

1. Select the option type (Call or Put)
2. Enter the required parameters:
   - Current Stock Price (S)
   - Strike Price (K)
   - Time to Maturity (in days)
   - Risk-free Rate (r)
   - Volatility (σ)
3. View the calculated option price
4. Explore sensitivity analysis graphs to understand how different parameters affect the option price

## Contributing

Feel free to fork this repository and submit pull requests for any improvements. You can also open issues for any bugs found or features you'd like to suggest.

## Acknowledgments

- Original Black-Scholes implementation inspired by QuantPy

## License

This project is licensed under the MIT License - see the LICENSE file for details.

[MIT](https://choosealicense.com/licenses/mit/)


