import pandas as pd
import numpy as np

class Parser:
    def __init__(self) -> None:
        pass

    def parse_bac_cc_stmt(csv_path: str) -> pd.DataFrame:
        """Parses BAC Credomatic credit card statement.

        Args:
            csv_path (str): The path to the CSV file to parse.

        Returns:
            pd.DataFrame: A Pandas DataFrame with 4 columns 
            ['date', 'transaction_description', 'currency', 'amount']
        """
        # Read CSV
        df_stmt = pd.read_csv(csv_path, header=None)

        # Drop unused columns
        df_stmt = df_stmt.drop(labels=[4,5,6,7,8], axis=1)

        # Rename cols
        rename_cols = {
            0: 'date',
            1: 'transaction_description',
            2: 'amount_hnl',
            3: 'amount_usd'
        }

        df_stmt = df_stmt.rename(columns=rename_cols)

        # Parse dates, only rows with dates are valid entries
        df_stmt['date'] = pd.to_datetime(df_stmt['date'], format='%d/%m/%Y', errors='coerce') 

        # Drop the date rows with NaN/NaT values  
        df_stmt = df_stmt.dropna(subset=['date'])

        # Convert the transaction amounts to numeric. Determine currency. Convert into one column
        # I have never seen a transaction that has both HNL and USD so addition shold be good enough
        # Invert the sign because expenses are positive in this statement
        df_stmt['amount_hnl'] = pd.to_numeric(df_stmt['amount_hnl'], errors='coerce')
        df_stmt['amount_usd'] = pd.to_numeric(df_stmt['amount_usd'], errors='coerce')
        df_stmt['currency'] = np.where(df_stmt['amount_usd']==0, 'HNL', 'USD')
        df_stmt['amount'] = (df_stmt['amount_hnl'] + df_stmt['amount_usd']) * -1.0

        # Drop the original ammount columnts
        df_stmt = df_stmt.drop(labels=['amount_hnl', 'amount_usd'], axis=1)

        return df_stmt
    
    def parse_bac_acc_stmt(csv_path: str) -> pd.DataFrame:
        """Parses a BAC Credomatic bank account statement. 

        Args:
            csv_path (str): The path to CSV file to parse.

        Raises:
            ValueError: Raises ValueError if currency is not in ['HNL', 'USD']

        Returns:
            pd.DataFrame: A Pandas DataFrame with 4 columns 
            ['date', 'reference_number', 'transaction_description', 'currency', 'amount']
        """
        # Read CSV
        df_stmt = pd.read_csv(csv_path, header=None)

        # Get currency
        currency = df_stmt.iloc[1, 3].strip()

        # Drop unused columns
        df_stmt = df_stmt.drop(labels=[6,7,8,9,10,11,12,13,14,15,16], axis=1)

        # Rename cols
        rename_cols = {
            0: 'date',
            1: 'reference_number',
            2: 'code',
            3: 'transaction_description',
            4: 'amount_debit',
            5: 'amount_credit'
        }

        df_stmt = df_stmt.rename(columns=rename_cols)

        # Parse dates, only rows with dates are valid entries
        df_stmt['date'] = pd.to_datetime(df_stmt['date'], format='%d/%m/%Y', errors='coerce') 

        # Drop the date rows with NaN/NaT values  
        df_stmt = df_stmt.dropna(subset=['date'])

        # Convert the transaction amounts to numeric. Debits are negative and credits positive
        df_stmt['amount_debit'] = pd.to_numeric(df_stmt['amount_debit'], errors='coerce')
        df_stmt['amount_credit'] = pd.to_numeric(df_stmt['amount_credit'], errors='coerce')
        df_stmt['amount'] = (df_stmt['amount_debit'] * -1.0) + df_stmt['amount_credit']

        # Drop the original amount columnts
        df_stmt = df_stmt.drop(labels=['amount_debit', 'amount_credit', 'code'], axis=1)

        # Add currency raise error if standard currency cannot be found raise error
        if currency == 'USD':
            df_stmt['currency'] = 'USD'
        elif currency == 'LPS':
            df_stmt['currency'] = 'HNL'
        else:
            raise ValueError(f'Currency {currency} is not supported.')

        return df_stmt