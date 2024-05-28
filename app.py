# app.py
from flask import Flask, request, jsonify, send_from_directory
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
from models import Expense

app = Flask(__name__)

BASE_URL = 'http://strapi.koders.in/api/expenses/'

@app.route('/')
def index():
    return "Welcome to the Expense Tracker API"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# CRUD operations
@app.route('/expenses', methods=['POST'])
def create_expense():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        print("Received data:", data)  # Debugging statement

        expense = Expense.from_dict({'attributes': data})
        payload = {"data": expense.to_dict()}
        print("Payload being sent to Strapi:", payload)  # Debugging statement
        response = requests.post(BASE_URL, json=payload)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print("Exception:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/expenses', methods=['GET'])
def get_expenses():
    try:
        response = requests.get(BASE_URL)
        expenses = response.json()
        return jsonify(expenses), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/expenses/<id>', methods=['PUT'])
def update_expense(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        print("Received data:", data)  # Debugging statement

        expense = Expense.from_dict({'attributes': data})
        payload = {"data": expense.to_dict()}
        print("Payload being sent to Strapi:", payload)  # Debugging statement
        response = requests.put(f"{BASE_URL}{id}", json=payload)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print("Exception:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/expenses/<id>', methods=['DELETE'])
def delete_expense(id):
    try:
        response = requests.delete(f"{BASE_URL}{id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print("Exception:", e)
        return jsonify({'error': str(e)}), 500

# Scheduler for updating recurring expenses
def update_recurring_expenses():
    try:
        response = requests.get(BASE_URL)
        expenses = response.json()

        for expense_data in expenses['data']:
            expense = Expense.from_dict(expense_data)
            if expense.frequency != 'One-Time':
                increment = 0
                base = expense.base
                frequency = expense.frequency

                if frequency == 'Daily':
                    increment = base
                elif frequency == 'Weekly':
                    increment = base / 7
                elif frequency == 'Monthly':
                    increment = base / 30
                elif frequency == 'Quarterly':
                    increment = base / 90
                elif frequency == 'Yearly':
                    increment = base / 365

                expense.amount += increment
                payload = {"data": expense.to_dict()}
                print("Payload being sent to Strapi:", payload)  # Debugging statement
                requests.put(f"{BASE_URL}{expense_data['id']}", json=payload)

    except Exception as e:
        print(f"Error updating recurring expenses: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(update_recurring_expenses, 'cron', hour=0, minute=0)
scheduler.start()

if __name__ == '__main__':
    app.run(port=5000)
