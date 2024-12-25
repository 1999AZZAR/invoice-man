import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_create_invoice():
    response = requests.post(f"{BASE_URL}/invoices", json={
        "invoice_number": "INV-001",
        "buyer_name": "John Doe",
        "buyer_address": "123 Main Street",
        "issue_date": "2024-12-01",
        "items": "Laptop, Mouse",
        "quantity": 2,
        "unit_price": 750.50,
        "subtotal": 1501.00,
        "discount": 50.00,
        "shipping_cost": 20.00,
        "total_amount": 1471.00
    })
    assert response.status_code == 201
    assert response.json()["message"] == "Invoice created successfully."

def test_get_invoices():
    response = requests.get(f"{BASE_URL}/invoices?buyer_name=John Doe")
    assert response.status_code == 200
    assert response.json()["message"] == "Invoices retrieved successfully."

def test_delete_invoice():
    response = requests.delete(f"{BASE_URL}/invoices/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Invoice 1 deleted successfully."
