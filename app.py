# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation: Retrieves and displays all transactions
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Create operation: Adds a new transaction
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        # Add new transaction using form field values
        transaction = {
            "id": len(transactions) + 1,
            "date": request.form["date"],
            "amount": float(request.form["amount"])
        }
        # Add transaction to the existing transactions
        transactions.append(transaction)

        # Redirect user back to transaction page
        return redirect(url_for("get_transactions"))

    elif request.method == "GET":
        # Render form to display add transaction form
        return render_template("form.html")

# Update operation: Edits an existing transaction
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == "GET":
        # Render form to display edit transaction form
        for transaction in transactions:
            if transaction["id"] == transaction_id:
                return render_template("edit.html", transaction=transaction)

    elif request.method == "POST":
        # Pull data from the edit form fields and save into variables
        date = request.form["date"]
        amount = request.form["amount"]

        # Find the transaction being edited and update its values with the form data
        for transaction in transactions:
            if transaction["id"] == transaction_id:
                transaction["date"] = date
                transaction["amount"] = amount
                # Exit early if transaction is found
                break

        # Redirect to transactions list page after edit is complete
        return redirect(url_for("get_transactions"))

# Delete operation: Removes a transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        # Find transaction with the matching ID and remove it from the list
        if transaction["id"] == transaction_id:
            transactions.remove(transaction)
            # Stop searching if found before reaching end of list data
            break

    # Redirect to transactions list page after delete is complete
    return redirect(url_for("get_transactions"))

# Search operation: Filters transactions based on amount range
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        min_amt = float(request.form["min_amount"])
        max_amt = float(request.form["max_amount"])
        filtered_transactions = [transaction for transaction in transactions if min_amt <= transaction["amount"] <= max_amt]
        return render_template("transactions.html", transactions=filtered_transactions)
    elif request.method == "GET":
        return render_template("search.html", transactions=transactions)

# Balance operation: Calculates and displays total balance of all transactions
@app.route("/balance")
def total_balance():
    balance = sum(transaction["amount"] for transaction in transactions)
    return render_template("transactions.html", transactions=transactions, total_balance=balance)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)