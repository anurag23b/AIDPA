def analyze_finance(query: str):
    # Mock NLP + Categorization
    if "expenses" in query:
        return {
            "summary": "Expenses for July: ₹12,000 split across Rent, Food, Travel",
            "chart": {
                "labels": ["Rent", "Food", "Travel"],
                "values": [6000, 4000, 2000],
            }
        }
    return {"summary": "No matching records", "chart": {}}

def get_forecast():
    return {
        "labels": ["Aug", "Sep", "Oct"],
        "predicted_savings": [1500, 2000, 1800],
        "predicted_expenses": [10000, 9500, 11000]
    }
