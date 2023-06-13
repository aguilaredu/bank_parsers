# Bank Parsers

## Introduction
Set of CSV parsers to parse crappy bank statement exports. Why are they so bad really?

## Usage
Project contains one `Parser` class with different methods for each type of statement to process. Currently the following methods are implemented:
`parse_bac_acc_stmt()` -> Parses BAC Credomatic bank account statements for both HNL and USD. Other currencies are not supported. BAC's export is not UTF-8 encoded which causes issues with the DataFrame creation. Currently, the file has to be converted to UTF-8 before feeding it to the method.
`parse_bac_cc_stmt` -> Parses BAC Credomatic credit cart statements. 
