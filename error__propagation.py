import pandas as pd
import numpy as np
import sympy as sp
from joblib import Parallel, delayed

def simulate_row(row, variables, expr, n_samples):
    """
    Simulates values for a row based on the uncertainties of variables and a given expression.
    
    Parameters:
    - row: A pandas Series object containing the values for the variables and their uncertainties.
    - variables: A list of the names of the variables involved in the simulation.
    - expr: A sympy expression representing the function to evaluate.
    - n_samples: The number of samples to simulate.
    
    Returns:
    - A tuple containing the mean and the standard deviation of the simulated values, rounded to 3 decimals.
    """
    simulated_values = []
    for _ in range(n_samples):
        # Generate a simulated value for each variable based on its mean and uncertainty
        simulated_row = {var: np.random.normal(row[var], row['D'+var]) for var in variables}
        
        # Substitute the simulated values into the expression and evaluate the result
        expr_sub = expr.subs(simulated_row)
        
        # Store the result of the evaluation
        simulated_values.append(float(expr_sub))
    
    # Calculate and return the mean and standard deviation of the simulated results
    f_mean = np.mean(simulated_values)
    f_std = np.std(simulated_values)
    
    return round(f_mean, 3), round(f_std, 3)

def montecarlo_error_propagation(df, function_str, n_samples=1000):
    """
    Performs error propagation using the Monte Carlo method.
    
    Parameters:
    - df: A pandas DataFrame containing the values for the variables and their uncertainties.
    - function_str: A string representing the mathematical function to evaluate.
    - n_samples: The number of samples to simulate for each row (default is 1000).
    
    Returns:
    - A DataFrame with the results of the simulation, including the mean and error of the evaluated function.
    """
    # Convert the function string into a sympy expression and extract the variable names
    expr = sp.sympify(function_str)
    variables = [col for col in df.columns if not col.startswith('D')]
    
    # Prepare the results DataFrame
    df_result = df.copy()
    df_result['f'] = 0.0
    df_result['f_error'] = 0.0
    
    # Execute simulations in parallel and store the results in the DataFrame
    results = Parallel(n_jobs=-1)(delayed(simulate_row)(row, variables, expr, n_samples) for index, row in df.iterrows())
    for i, (f_mean, f_std) in enumerate(results):
        df_result.at[i, 'f'] = f_mean
        df_result.at[i, 'f_error'] = f_std
    
    return df_result
