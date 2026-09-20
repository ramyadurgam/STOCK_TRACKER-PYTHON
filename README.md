📈 Stock Portfolio Tracker

A colourful, console-based Stock Portfolio Tracker written in Python, built for the CodeAlpha Python Programming Internship (Task 2).

Enter the stocks you own and how many shares of each. The program looks up every price, calculates your total investment value, shows a neat table, and can save the result to a .txt or .csv file.

✨ Features
Add stocks by symbol or company name (AAPL or apple)
Prices come from a hardcoded dictionary of 10 sample US stocks
Calculates the total investment value (quantity × price, summed)
Table sorted by value, with share bars and percentages
Typo suggestions: typing appl gives "Did you mean AAPL (Apple)?"
Adding the same stock twice merges the quantities
Input validation for unknown stocks and invalid quantities
Saves the result as .txt, .csv, or both
Coloured output (set NO_COLOR=1 for plain text)
🧠 Concepts Used
Concept	Where it is used
Dictionary	STOCK_PRICES, COMPANIES and the portfolio itself
Input / output	input() prompts and formatted print()
Basic arithmetic	value = quantity × price, totals, percentages
File handling	save_txt() and save_csv()
Functions, loops, try/except	menu loop, validation, safe file saving
🚀 How to Run
bash
python stock_tracker.py

Requirements: Python 3.6 or newer. No external libraries needed.

🎮 Commands
Input	Action
stock name or symbol	add a stock, then enter its quantity
list	show all available stocks and prices
done	finish and see the portfolio
back (at the quantity prompt)	cancel adding that stock
💵 Available Stocks (sample prices in USD)
Symbol	Company	Price	Symbol	Company	Price
AAPL	Apple	$180	NFLX	Netflix	$400
TSLA	Tesla	$250	AMD	AMD	$110
GOOGL	Google	$140	ORCL	Oracle	$120
MSFT	Microsoft	$330	AMZN	Amazon	$130
NVDA	Nvidia	$450	META	Meta	$300

⚠️ Prices are sample values for learning only, not live market data.

🖥️ Sample Session
  ➤ Stock name/symbol (list / done): appl
  'appl' not found. Did you mean AAPL (Apple)?
  ➤ Stock name/symbol (list / done): aapl
  ➤ How many shares of AAPL? (or 'back'): 10
  Added 10 x AAPL (Apple) @ $180.00 = $1,800.00
  Running total: $1,800.00
  ➤ Stock name/symbol (list / done): tesla
  ➤ How many shares of TSLA? (or 'back'): 5
  Added 5 x TSLA (Tesla) @ $250.00 = $1,250.00
  Running total: $3,050.00
  ➤ Stock name/symbol (list / done): aapl
  ➤ How many shares of AAPL? (or 'back'): 5
  Added 5 x AAPL (Apple) @ $180.00 = $900.00
  Running total: $3,950.00
  ➤ Stock name/symbol (list / done): done
Final Output
  STOCK      QTY       PRICE          VALUE   SHARE
  ──────────────────────────────────────────────────────────────
  AAPL        15     $180.00      $2,700.00   ███████░░░  68.4%
  TSLA         5     $250.00      $1,250.00   ███░░░░░░░  31.6%
  ──────────────────────────────────────────────────────────────
  TOTAL       20                  $3,950.00

  ╔══════════════════════════════════════════════════════════════╗
  ║                    TOTAL INVESTMENT VALUE                    ║
  ║                          $3,950.00                           ║
  ╚══════════════════════════════════════════════════════════════╝

  Stocks held : 2
  Largest     : AAPL (Apple) - $2,700.00
💾 Saved Files

Choose 1) .txt, 2) .csv, or 3) Both after the summary. Files are saved in the folder where you run the program.

portfolio_summary.txt

CodeAlpha - Stock Portfolio Tracker
Generated: 20 Sep 2026, 11:19 AM
--------------------------------------------------------------
STOCK      QTY       PRICE          VALUE   SHARE
--------------------------------------------------------------
GOOGL       12     $140.00      $1,680.00   ######....  55.4%
NVDA         3     $450.00      $1,350.00   ####......  44.6%
--------------------------------------------------------------
TOTAL INVESTMENT VALUE: $3,030.00

portfolio_summary.csv (opens directly in Excel)

Stock,Company,Quantity,Price (USD),Value (USD),Share (%)
GOOGL,Google,12,140.00,1680.00,55.4
NVDA,Nvidia,3,450.00,1350.00,44.6
TOTAL,,15,,3030.00,100.0
✅ Input Handling
You type	Result
unknown stock (xyz)	not available, type list to see all stocks
typo (appl)	suggests the closest match
abc or 2.5 as quantity	asks for a whole number
0 or a negative number	asks for a number greater than 0
done with no stocks added	asks you to add at least one stock
Ctrl+C / Ctrl+D	exits politely
📁 Project Structure
CodeAlpha_StockPortfolioTracker/
├── stock_tracker.py
└── README.md
👤 Author
Your Name: RAMYA DURGAM
