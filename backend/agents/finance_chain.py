# backend/agents/finance_chain.py
def run_finance_chain(query: str) -> str:
    if "spend" in query.lower():
        return "This week you spent ₹4,520. Biggest expense: Food delivery."
    elif "save" in query.lower():
        return "You saved ₹1,200 this month. Consider increasing SIP by ₹500."
    elif "invest" in query.lower():
        return "Mutual funds and Nifty50 ETFs are ideal for your profile."
    return "Please specify a finance-related query like spending, saving, or investing."
