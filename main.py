import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
import os
# also install openpyxl as a requirement

def get_stock_data(stock_ticker):
    try:
        # Fetch daily historical data for the specified ticker
        pfe = yf.Ticker(stock_ticker)
        hist = pfe.history(period="max")

        # Check if the DataFrame is empty
        if hist.empty:
            print(f"No data found for the ticker '{stock_ticker}'. Please check the ticker symbol.")
            raise Exception(f"No data found for the ticker '{stock_ticker}'. Please check the ticker symbol.")

        # Filepath for the CSV file
        output_file = f"{stock_ticker}_historical_data.csv"

        # If the file exists, remove it before saving
        if os.path.exists(output_file):
            os.remove(output_file)

        # Save to CSV if data is valid
        hist.to_csv(output_file)

        print(hist.head(1))
        return hist

    except Exception as e:
        print(e)
        raise

def calculate_percentage_daily_variation(hist, stock_ticker):
    try:
        # Remove rows with Open price equal to 0 to avoid division by zero
        hist = hist[hist['Open'] != 0]

        # Calculate the percentage daily variation and add it as a new column
        hist['Percentage_Daily_Variation'] = 100 * (hist['Open'] - hist['Close']) / hist['Open']
        print(hist.head(1))

        # Remove timezone information from the index if it exists
        if pd.api.types.is_datetime64_any_dtype(hist.index):
            hist.index = hist.index.tz_localize(None)

        # Save the data to a new Excel file
        output_file = f'{stock_ticker}_historical_data_with_variation.xlsx'
        
        # If the file exists, remove it before saving
        if os.path.exists(output_file):
            os.remove(output_file)

        hist.to_excel(output_file, engine='openpyxl')
        print(f"Data saved to {output_file}")
        return hist
    
    except Exception as e:
        print(e)
        raise

def plot_histogram(hist):
    try:
        # Plotting the histogram for the percentage daily variation
        plt.figure(figsize=(10, 6))

        # Creating the histogram with a step of 0.1%
        plt.hist(hist['Percentage_Daily_Variation'].dropna(), bins=int((hist['Percentage_Daily_Variation'].max() - hist['Percentage_Daily_Variation'].min()) / 0.1), edgecolor='black', alpha=0.7)

        # Adding titles and labels
        plt.title('Histogram of Percentage Daily Variation of Pfizer Stock')
        plt.xlabel('Percentage Daily Variation (%)')
        plt.ylabel('Count of Days')

        # Marking max and min variation
        max_variation = hist['Percentage_Daily_Variation'].max()
        min_variation = hist['Percentage_Daily_Variation'].min()
        max_date = hist['Percentage_Daily_Variation'].idxmax()
        min_date = hist['Percentage_Daily_Variation'].idxmin()

        plt.axvline(max_variation, color='r', linestyle='--', label=f'Max Variation: {max_variation:.2f}% on {max_date.date()}')
        plt.axvline(min_variation, color='b', linestyle='--', label=f'Min Variation: {min_variation:.2f}% on {min_date.date()}')

        # Adding legend
        plt.legend()

        # Display the plot
        plt.show()

    except Exception as e:
        print(e)
        raise

def fit_and_plot_distribution(hist):
    try:
        # Fitting a normal distribution to the data
        variation_data = hist['Percentage_Daily_Variation'].dropna()

        # Fit a normal distribution
        mu, std = norm.fit(variation_data)

        # Create a range of values for the x-axis
        xmin, xmax = variation_data.min(), variation_data.max()
        x = np.linspace(xmin, xmax, 100)

        # Calculate the PDF (Probability Density Function) for the normal distribution
        p = norm.pdf(x, mu, std)

        # Plotting the model distribution on the same histogram
        plt.figure(figsize=(10, 6))

        # Histogram of the data
        plt.hist(variation_data, bins=int((variation_data.max() - variation_data.min()) / 0.1), density=True, alpha=0.6, color='g', edgecolor='black', label='Data Histogram')

        # Plotting the fitted distribution
        plt.plot(x, p, 'r-', linewidth=2, label=f'Normal Fit: μ={mu:.2f}, σ={std:.2f}')

        # Adding titles and labels
        plt.title('Histogram of Percentage Daily Variation with Fitted Normal Distribution')
        plt.xlabel('Percentage Daily Variation (%)')
        plt.ylabel('Density')
        plt.legend()

        # Display the plot
        plt.show()

    except Exception as e:
        print(e)
        raise

def main(stock_ticker):
    try:
        hist = get_stock_data(stock_ticker)
        hist = calculate_percentage_daily_variation(hist, stock_ticker)
        plot_histogram(hist)
        fit_and_plot_distribution(hist)
    except Exception as e:
        print(f"An error occurred while fetching data for '{stock_ticker}': {e}")

if __name__ == "__main__":
    stock_ticker = input("Enter the stock ticker symbol (e.g., PFE for Pfizer): ").upper()
    main(stock_ticker)
