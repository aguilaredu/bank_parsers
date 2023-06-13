import pandas as pd
import numpy as np

class Parser:
    def __init__(self) -> None:
        pass

    def bac_cc_stmt_parser(csv_path: str) -> pd.DataFrame:
        """Parses BAC Credomatic credit card statement.

        Args:
            csv_path (str): The path to the CSV file to parse.

        Returns:
            pd.DataFrame: A Pandas DataFrame with 4 columns 
            ['date', 'transaction_name', 'currency', 'amount']
        """
        # Read CSV
        df_stmt = pd.read_csv(csv_path, header=None)

        # Drop unused columns
        df_stmt = df_stmt.drop(labels=[4,5,6,7,8], axis=1)

        # Rename cols
        rename_cols = {
            0: 'date',
            1: 'transaction_name',
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
        df_stmt['amount_hnl'] = pd.to_numeric(df_stmt['amount_hnl'], errors='coerce')
        df_stmt['amount_usd'] = pd.to_numeric(df_stmt['amount_usd'], errors='coerce')
        df_stmt['currency'] = np.where(df_stmt['amount_usd']==0, 'HNL', 'USD')
        df_stmt['amount'] = df_stmt['amount_hnl'] + df_stmt['amount_usd']

        # Drop the original ammount columnts
        df_stmt = df_stmt.drop(labels=['amount_hnl', 'amount_usd'], axis=1)

        return df_stmt