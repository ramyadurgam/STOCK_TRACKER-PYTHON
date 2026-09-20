"""
CodeAlpha Python Programming Internship
Task 2: Stock Portfolio Tracker
------------------------------------------------------------
Enter stock names and quantities. The program looks up each price in a
hardcoded dictionary, calculates the total investment value, shows a
neat table, and can save the result to a .txt and/or .csv file.

Commands while adding stocks:
  <stock name or symbol>  add a stock   (e.g. AAPL or apple)
  list                    show all available stocks and prices
  done                    finish and see your portfolio

Tip: set NO_COLOR=1 to switch off colours.
"""

import csv
import datetime
import difflib
import os
import sys

WIDTH = 64

# Hardcoded stock prices in US dollars (sample prices, not live data)
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 140,
    "MSFT": 330,
    "AMZN": 130,
    "NVDA": 450,
    "META": 300,
    "NFLX": 400,
    "AMD": 110,
    "ORCL": 120,
}

# Company names so users can type "apple" as well as "AAPL"
COMPANIES = {
    "AAPL": "Apple",
    "TSLA": "Tesla",
    "GOOGL": "Google",
    "MSFT": "Microsoft",
    "AMZN": "Amazon",
    "NVDA": "Nvidia",
    "META": "Meta",
    "NFLX": "Netflix",
    "AMD": "AMD",
    "ORCL": "Oracle",
}

TXT_FILE = "portfolio_summary.txt"
CSV_FILE = "portfolio_summary.csv"

# ------------------------------------------------------------------
#  Colour helpers
# ------------------------------------------------------------------
USE_COLOR = (sys.stdout.isatty() or "FORCE_COLOR" in os.environ) \
    and "NO_COLOR" not in os.environ

if os.name == "nt":
    os.system("")  # lets Windows terminals understand colour codes

CODES = {
    "reset": "\033[0m", "bold": "\033[1m", "dim": "\033[2m",
    "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m",
    "blue": "\033[94m", "magenta": "\033[95m", "cyan": "\033[96m",
}


def paint(text, *styles):
    """Wrap text in colour/style codes (does nothing if colour is off)."""
    if not USE_COLOR:
        return text
    return "".join(CODES[s] for s in styles) + text + CODES["reset"]


def visible_len(text):
    """Length of text as seen on screen (ignores colour codes)."""
    length = 0
    skipping = False
    for ch in text:
        if ch == "\033":
            skipping = True
        elif skipping and ch == "m":
            skipping = False
        elif not skipping:
            length += 1
    return length


def center(text, width):
    space = width - visible_len(text)
    left = space // 2
    return " " * left + text + " " * (space - left)


def box(lines, color):
    """Draw a double-line box around a list of text lines."""
    inner = WIDTH - 2
    out = [paint("╔" + "═" * inner + "╗", color)]
    for line in lines:
        out.append(paint("║", color) + center(line, inner) + paint("║", color))
    out.append(paint("╚" + "═" * inner + "╝", color))
    return out


def say(message, color="yellow"):
    print("  " + paint(message, color, "bold"))


# ------------------------------------------------------------------
#  Portfolio logic
# ------------------------------------------------------------------
def money(amount):
    return f"${amount:,.2f}"


def resolve_stock(text):
    """Turn user text (symbol or company name) into a stock symbol, or None."""
    cleaned = text.strip()
    if cleaned.upper() in STOCK_PRICES:
        return cleaned.upper()
    for symbol, company in COMPANIES.items():
        if cleaned.lower() == company.lower():
            return symbol
    return None


def suggest_stock(text):
    """Return the closest known stock symbol for a typo, or None."""
    choices = {}
    for symbol, company in COMPANIES.items():
        choices[symbol.lower()] = symbol
        choices[company.lower()] = symbol
    matches = difflib.get_close_matches(text.strip().lower(), list(choices), n=1, cutoff=0.6)
    if matches:
        return choices[matches[0]]
    return None


def ask_quantity(symbol):
    """Ask for a whole number greater than 0. Returns None if cancelled."""
    while True:
        raw = input(f"  ➤ How many shares of {symbol}? (or 'back'): ").strip().lower()
        if raw in ("back", "cancel"):
            return None
        try:
            quantity = int(raw.replace(",", ""))
        except ValueError:
            say("Please enter a whole number, e.g. 10.", "red")
            continue
        if quantity <= 0:
            say("Quantity must be greater than 0.", "red")
        elif quantity > 1_000_000:
            say("That is too large. Please enter 1,000,000 or fewer.", "red")
        else:
            return quantity


def calculate_rows(portfolio):
    """Return (rows, total). Each row is (symbol, quantity, price, value)."""
    rows = []
    total = 0
    for symbol, quantity in portfolio.items():
        price = STOCK_PRICES[symbol]
        value = quantity * price
        total += value
        rows.append((symbol, quantity, price, value))
    rows.sort(key=lambda row: row[3], reverse=True)  # biggest holding first
    return rows, total


# ------------------------------------------------------------------
#  Display helpers
# ------------------------------------------------------------------
def show_available():
    print()
    print("  " + paint("AVAILABLE STOCKS", "bold", "cyan") +
          paint("  (sample prices in USD)", "dim"))
    symbols = list(STOCK_PRICES)
    for start in range(0, len(symbols), 3):
        cells = []
        for symbol in symbols[start:start + 3]:
            cell = paint(f"{symbol:<6}", "bold", "cyan") + paint(f"{money(STOCK_PRICES[symbol]):>9}", "green")
            cells.append(cell + "    ")
        print("    " + "".join(cells))
    print()


def row_parts(row, total, full="█", empty="░"):
    """Plain-text pieces of one table row."""
    symbol, quantity, price, value = row
    share = value / total
    filled = round(share * 10)
    return (f"{symbol:<8}", f"{quantity:>6,}", f"{money(price):>12}",
            f"{money(value):>15}", full * filled + empty * (10 - filled),
            f"{share * 100:5.1f}%")


def print_summary(rows, total):
    print()
    for line in box([paint("YOUR PORTFOLIO", "bold", "cyan")], "cyan"):
        print("  " + line)
    print()
    head = f"{'STOCK':<8}{'QTY':>6}{'PRICE':>12}{'VALUE':>15}   SHARE"
    print("  " + paint(head, "bold", "yellow"))
    print("  " + paint("─" * (WIDTH - 2), "dim"))
    for row in rows:
        sym, qty, price, value, bar, pct = row_parts(row, total)
        print("  " + paint(sym, "bold", "cyan") + qty + paint(price, "dim") +
              paint(value, "green") + "   " + paint(bar, "magenta") + " " + pct)
    print("  " + paint("─" * (WIDTH - 2), "dim"))

    total_shares = sum(row[1] for row in rows)
    print(f"  {'TOTAL':<8}{total_shares:>6,}{'':>12}" + paint(f"{money(total):>15}", "bold", "green"))
    print()
    banner = [paint("TOTAL INVESTMENT VALUE", "bold"),
              paint(money(total), "bold", "green")]
    for line in box(banner, "green"):
        print("  " + line)
    largest = rows[0]
    print()
    print(f"  Stocks held : {len(rows)}")
    print(f"  Largest     : {largest[0]} ({COMPANIES[largest[0]]}) - {money(largest[3])}")
    print()


# ------------------------------------------------------------------
#  File saving
# ------------------------------------------------------------------
def save_txt(rows, total):
    now = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    lines = [
        "CodeAlpha - Stock Portfolio Tracker",
        f"Generated: {now}",
        "-" * 62,
        f"{'STOCK':<8}{'QTY':>6}{'PRICE':>12}{'VALUE':>15}   SHARE",
        "-" * 62,
    ]
    for row in rows:
        sym, qty, price, value, bar, pct = row_parts(row, total, "#", ".")
        lines.append(f"{sym}{qty}{price}{value}   {bar} {pct}")
    lines.append("-" * 62)
    lines.append(f"TOTAL INVESTMENT VALUE: {money(total)}")
    with open(TXT_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")
    return os.path.abspath(TXT_FILE)


def save_csv(rows, total):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Stock", "Company", "Quantity", "Price (USD)", "Value (USD)", "Share (%)"])
        for symbol, quantity, price, value in rows:
            writer.writerow([symbol, COMPANIES[symbol], quantity,
                             f"{price:.2f}", f"{value:.2f}", f"{value / total * 100:.1f}"])
        writer.writerow(["TOTAL", "", sum(row[1] for row in rows), "", f"{total:.2f}", "100.0"])
    return os.path.abspath(CSV_FILE)


def ask_save(rows, total):
    print("  " + paint("SAVE YOUR RESULT?", "bold", "cyan"))
    print("    1) Text file (.txt)")
    print("    2) CSV file (.csv)")
    print("    3) Both")
    print("    4) No, thanks")
    while True:
        choice = input("  ➤ Choose 1-4: ").strip()
        if choice in ("1", "2", "3", "4"):
            break
        say("Please type 1, 2, 3 or 4.", "red")

    try:
        if choice in ("1", "3"):
            say("Saved: " + save_txt(rows, total), "green")
        if choice in ("2", "3"):
            say("Saved: " + save_csv(rows, total), "green")
    except OSError as error:
        say(f"Could not save the file: {error}", "red")


# ------------------------------------------------------------------
#  Main program
# ------------------------------------------------------------------
def collect_portfolio():
    """Ask the user for stocks until they type 'done'."""
    portfolio = {}
    while True:
        entry = input("  ➤ Stock name/symbol (list / done): ").strip()
        command = entry.lower()

        if command == "":
            continue

        if command == "list":
            show_available()

        elif command == "done":
            if portfolio:
                return portfolio
            say("Add at least one stock first.", "yellow")

        else:
            symbol = resolve_stock(entry)
            if symbol is None:
                guess = suggest_stock(entry)
                if guess:
                    say(f"'{entry}' not found. Did you mean {guess} ({COMPANIES[guess]})?", "yellow")
                else:
                    say(f"'{entry}' is not available. Type 'list' to see all stocks.", "red")
                continue

            quantity = ask_quantity(symbol)
            if quantity is None:
                continue
            portfolio[symbol] = portfolio.get(symbol, 0) + quantity
            price = STOCK_PRICES[symbol]
            say(f"Added {quantity:,} x {symbol} ({COMPANIES[symbol]}) @ {money(price)} "
                f"= {money(quantity * price)}", "green")
            running = sum(qty * STOCK_PRICES[sym] for sym, qty in portfolio.items())
            print("  " + paint(f"Running total: {money(running)}", "dim"))


def main():
    print()
    title = [paint("★  STOCK PORTFOLIO TRACKER  ★", "bold", "cyan"),
             paint("CodeAlpha Python Internship · Task 2", "dim")]
    for line in box(title, "cyan"):
        print("  " + line)
    print()
    print("  Add the stocks you own, then type " + paint("done", "bold", "green") +
          " to see your total.")
    show_available()

    try:
        portfolio = collect_portfolio()
        rows, total = calculate_rows(portfolio)
        print_summary(rows, total)
        ask_save(rows, total)
    except (EOFError, KeyboardInterrupt):
        print("\n\n  Goodbye!\n")
        return

    print()
    say("Thank you for using the Stock Portfolio Tracker!", "cyan")
    print()


if __name__ == "__main__":
    main()
