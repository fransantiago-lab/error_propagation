# Monte Carlo Error Propagation

This project implements an error propagation method using Monte Carlo simulations. It is based on the theory that the uncertainties of a mathematical function can be estimated through the simulation of its input variables.

## Requirements

To run this code, you need Python 3.x and the following libraries:

- pandas
- numpy
- sympy
- joblib

You can install these dependencies with the following command:

```bash
pip install pandas numpy sympy joblib
```

## Usage

To use this code, you should have a pandas DataFrame that contains the variables of your function and their corresponding uncertainties. The uncertainties for each variable should be prefixed with 'D' (for example, 'Dx' for the uncertainty of 'x').

### Example

Imagine you have a DataFrame `df` with the following columns: `x`, `Dx`, `y`, `Dy`. You want to evaluate the function `f = x^2 + y^2` and its associated uncertainties using 1000 simulations per row. Here's how you could do it:

```python
import pandas as pd

# Your DataFrame here
df = pd.DataFrame({
    'x': [1, 2, 3],
    'Dx': [0.1, 0.2, 0.1],
    'y': [4, 5, 6],
    'Dy': [0.2, 0.2, 0.1]
})

result_df = montecarlo_error_propagation(df, 'x**2 + y**2', n_samples=1000)

print(result_df)
```

This command will print a DataFrame that includes the original columns along with `f` and `f_error`, representing the mean and standard deviation of the evaluated function.



This README file provides a clear guide on how to use the provided code, including a practical example to illustrate its usage.

