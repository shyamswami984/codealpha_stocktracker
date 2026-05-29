# ============================================================
#  Stock Portfolio Tracker — Indian Rupees (₹ INR)
#  Concepts: dictionary, input/output, arithmetic, file handling
# ============================================================

import csv
import os
from datetime import datetime

# -----------------------------------------------------------
# 1. USD → INR conversion rate (approx.)
# -----------------------------------------------------------
USD_TO_INR = 83.5

# -----------------------------------------------------------
# 2. HARDCODED STOCK PRICE DICTIONARY (prices in ₹ INR)
#    Indian stocks: NSE/BSE direct prices
#    US stocks: converted from USD to INR
# -----------------------------------------------------------
STOCK_PRICES = {
    # --- Indian Stocks (NSE / BSE) ---
    "RELIANCE":  2945.00,   # Reliance Industries
    "TCS":       3820.00,   # Tata Consultancy Services
    "INFY":      1650.00,   # Infosys Ltd.
    "HDFCBANK":  1720.00,   # HDFC Bank
    "WIPRO":      480.00,   # Wipro Ltd.
    "ICICIBANK": 1235.00,   # ICICI Bank
    "SBIN":       815.00,   # State Bank of India
    "TATAMOTORS":1020.00,   # Tata Motors

    # --- US Stocks (converted: USD × USD_TO_INR) ---
    "AAPL": round(182.50 * USD_TO_INR, 2),   # Apple Inc.
    "TSLA": round(248.00 * USD_TO_INR, 2),   # Tesla Inc.
    "MSFT": round(415.00 * USD_TO_INR, 2),   # Microsoft Corp.
    "NVDA": round(875.40 * USD_TO_INR, 2),   # NVIDIA Corp.
}

STOCK_NAMES = {
    "RELIANCE":   "Reliance Industries",
    "TCS":        "Tata Consultancy Services",
    "INFY":       "Infosys Ltd.",
    "HDFCBANK":   "HDFC Bank",
    "WIPRO":      "Wipro Ltd.",
    "ICICIBANK":  "ICICI Bank",
    "SBIN":       "State Bank of India",
    "TATAMOTORS": "Tata Motors",
    "AAPL":       "Apple Inc. (US)",
    "TSLA":       "Tesla Inc. (US)",
    "MSFT":       "Microsoft Corp. (US)",
    "NVDA":       "NVIDIA Corp. (US)",
}

# -----------------------------------------------------------
# 3. HELPER: format number in Indian style (₹ X,XX,XXX.XX)
# -----------------------------------------------------------
def inr_format(amount):
    """Format a float as Indian Rupee string: ₹1,23,456.78"""
    s = f"{amount:.2f}"
    integer, decimal = s.split(".")
    # Indian grouping: last 3 digits, then groups of 2
    if len(integer) > 3:
        last3 = integer[-3:]
        rest = integer[:-3]
        groups = []
        while len(rest) > 2:
            groups.append(rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.append(rest)
        groups.reverse()
        integer = ",".join(groups) + "," + last3
    return f"₹{integer}.{decimal}"


# -----------------------------------------------------------
# 4. DISPLAY AVAILABLE STOCKS
# -----------------------------------------------------------
def show_available_stocks():
    print("\n" + "=" * 55)
    print(f"  {'TICKER':<12} {'COMPANY':<26} {'PRICE (₹)':>12}")
    print("=" * 55)
    for ticker, price in STOCK_PRICES.items():
        print(f"  {ticker:<12} {STOCK_NAMES[ticker]:<26} {inr_format(price):>12}")
    print("=" * 55)
    print(f"  (US stocks converted at 1 USD = ₹{USD_TO_INR})")
    print("=" * 55)


# -----------------------------------------------------------
# 5. GET PORTFOLIO INPUT FROM USER
# -----------------------------------------------------------
def get_portfolio_from_user():
    portfolio = {}   # dictionary: { 'TICKER': quantity }
    print("\nEnter your stock holdings. Type 'DONE' when finished.\n")

    while True:
        ticker = input("  Stock ticker (e.g. TCS, INFY, AAPL): ").strip().upper()

        if ticker == "DONE":
            break

        if ticker not in STOCK_PRICES:
            print(f"  ⚠  '{ticker}' not found. Available: {', '.join(STOCK_PRICES)}\n")
            continue

        try:
            qty = int(input(f"  Quantity of {ticker}: ").strip())
            if qty <= 0:
                print("  ⚠  Quantity must be a positive integer.\n")
                continue
        except ValueError:
            print("  ⚠  Please enter a valid whole number.\n")
            continue

        portfolio[ticker] = portfolio.get(ticker, 0) + qty
        print(f"  ✔  Added {ticker} × {qty}\n")

    return portfolio


# -----------------------------------------------------------
# 6. CALCULATE INVESTMENT VALUES
# -----------------------------------------------------------
def calculate_investment(portfolio):
    breakdown = []
    total = 0.0

    for ticker, qty in portfolio.items():
        price = STOCK_PRICES[ticker]        # dictionary lookup
        value = price * qty                 # basic arithmetic
        breakdown.append((ticker, qty, price, value))
        total += value

    return breakdown, total


# -----------------------------------------------------------
# 7. DISPLAY RESULTS
# -----------------------------------------------------------
def display_results(breakdown, total):
    print("\n" + "=" * 68)
    print("  PORTFOLIO SUMMARY (₹ INR)")
    print("=" * 68)
    print(f"  {'TICKER':<12} {'QTY':>6}  {'PRICE (₹)':>14}  {'VALUE (₹)':>16}")
    print("-" * 68)
    for ticker, qty, price, value in breakdown:
        print(f"  {ticker:<12} {qty:>6}  {inr_format(price):>14}  {inr_format(value):>16}")
    print("-" * 68)
    print(f"  {'TOTAL INVESTMENT':>32}   {inr_format(total):>16}")
    print("=" * 68)


# -----------------------------------------------------------
# 8. FILE HANDLING — save as TXT
# -----------------------------------------------------------
def save_to_txt(breakdown, total, filename="portfolio_result_inr.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("STOCK PORTFOLIO TRACKER (INR)\n")
        f.write(f"Generated  : {timestamp}\n")
        f.write(f"USD/INR    : 1 USD = ₹{USD_TO_INR}\n")
        f.write("=" * 60 + "\n")
        f.write(f"{'Ticker':<12} {'Qty':>6}  {'Price (₹)':>14}  {'Value (₹)':>16}\n")
        f.write("-" * 60 + "\n")
        for ticker, qty, price, value in breakdown:
            f.write(f"{ticker:<12} {qty:>6}  {inr_format(price):>14}  {inr_format(value):>16}\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'TOTAL':>34}   {inr_format(total):>16}\n")
    print(f"\n  ✔  Saved TXT → {os.path.abspath(filename)}")


# -----------------------------------------------------------
# 9. FILE HANDLING — save as CSV
# -----------------------------------------------------------
def save_to_csv(breakdown, total, filename="portfolio_result_inr.csv"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Stock Portfolio Tracker (INR)"])
        writer.writerow(["Generated", timestamp])
        writer.writerow([f"USD/INR Rate: 1 USD = Rs.{USD_TO_INR}"])
        writer.writerow([])
        writer.writerow(["Ticker", "Company", "Quantity", "Price (INR)", "Value (INR)"])
        for ticker, qty, price, value in breakdown:
            writer.writerow([ticker, STOCK_NAMES[ticker], qty,
                             f"{price:.2f}", f"{value:.2f}"])
        writer.writerow([])
        writer.writerow(["TOTAL", "", "", "", f"{total:.2f}"])
    print(f"  ✔  Saved CSV → {os.path.abspath(filename)}")


# -----------------------------------------------------------
# 10. MAIN PROGRAM
# -----------------------------------------------------------
def main():
    print("\n╔══════════════════════════════════════╗")
    print("║  STOCK PORTFOLIO TRACKER (₹ INR) 📈  ║")
    print("╚══════════════════════════════════════╝")

    show_available_stocks()

    portfolio = get_portfolio_from_user()

    if not portfolio:
        print("\n  No stocks entered. Exiting.")
        return

    breakdown, total = calculate_investment(portfolio)
    display_results(breakdown, total)

    save_choice = input("\n  Save results? [T]XT / [C]SV / [B]oth / [N]o: ").strip().upper()
    if save_choice in ("T", "B"):
        save_to_txt(breakdown, total)
    if save_choice in ("C", "B"):
        save_to_csv(breakdown, total)

    print("\n  Thank you for using Stock Portfolio Tracker!\n")


if __name__ == "__main__":
    main()
