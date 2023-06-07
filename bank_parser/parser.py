import pandas as pd

class Parser:
    def __init__(self) -> None:
        pass

    def bac_cc_stmt_parser(csv_path: str) -> pd.DataFrame:

        # File intake 
        df_stmt = pd.read_csv(csv_path)

        raise NotImplementedError