# Options Pricing Calculator

This repository contains a Python script for calculating the price of European call and put options using the Black-Scholes formula. The implementation is based on QuantPy's video tutorial on the Black-Scholes formula in Python.

## Table of Contents

- [Requirements](#requirements)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Requirements

To run this script, you need the following Python libraries:

- numpy
- scipy

You can install the required libraries using pip:

```sh
pip install numpy scipy
```

## Usage

To use the options pricing calculator, edit the script to enter the values for the variables: risk-free rate (r), spot price (S), strike price (K), time to maturity (T), and volatility (sigma).

```sh
# Example values
r = 0.01  # Risk-free rate
S = 30    # Spot price
K = 40    # Strike price
T = 240/365  # Time to maturity (in years)
sigma = 0.30  # Volatility
```

Then run the script to calculate the option price.

## How It Works

The script defines a function BS that calculates the Black-Scholes option price for a call or a put:

```sh
def BS(r, S, K, T, sigma, type='C'):
    "Calculate BS option price for a Call or a Put"
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    try:
        if type == "C":
            price = S * norm.cdf(d1, 0, 1) - K * np.exp(-r * T) * norm.cdf(d2, 0, 1)
        elif type == "P":
            price = K * np.exp(-r * T) * norm.cdf(-d2, 0, 1) - S * norm.cdf(-d1, 0, 1)
        return price    
    except:
        print('Confirm all values for variables')
```

## Example

Here's an example of how to use the script to calculate the price of a call option:

```sh
print('Option Price should be: ', round(BS(r, S, K, T, sigma, type="C"), 2))
```

This will output:
```sh
Option Price should be:  2.35
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue if you have any suggestions or improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.


