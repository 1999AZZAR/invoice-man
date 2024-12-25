### **Invoices API Test Calls**

#### **1. Create a New Invoice**
```bash
curl -X POST http://127.0.0.1:5000/invoices \
-H "Content-Type: application/json" \
-d '{
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
}'
```

#### **2. Retrieve All Invoices (With Pagination and Filters)**
```bash
curl -X GET "http://127.0.0.1:5000/invoices?buyer_name=John Doe&skip=0&limit=5"
```

#### **3. Retrieve a Single Invoice by ID**
```bash
curl -X GET http://127.0.0.1:5000/invoices/1
```

#### **4. Retrieve All data**
```bash
curl -X GET http://127.0.0.1:5000/invoices/all
```

#### **5. Update an Existing Invoice**
```bash
curl -X PUT http://127.0.0.1:5000/invoices/1 \
-H "Content-Type: application/json" \
-d '{
  "buyer_name": "Jane Doe",
  "discount": 100.00,
  "total_amount": 1391.00
}'
```

#### **6. Delete an Invoice by ID**
```bash
curl -X DELETE http://127.0.0.1:5000/invoices/1
```

---

### **Payments API Test Calls**

#### **1. Add a Payment to an Invoice**
```bash
curl -X POST http://127.0.0.1:5000/invoices/1/payments \
-H "Content-Type: application/json" \
-d '{
  "amount_paid": 500.00,
  "payment_date": "2024-12-02",
  "payment_method": "Credit Card"
}'
```

#### **2. Retrieve All Payments for an Invoice**
```bash
curl -X GET http://127.0.0.1:5000/invoices/1/payments
```

#### **3. Delete a Payment by ID**
```bash
curl -X DELETE http://127.0.0.1:5000/payments/1
```

---

### **Example API Responses**

#### **Create a New Invoice (Success)**
```json
{
  "message": "Invoice created successfully.",
  "data": {
    "id": 1,
    "invoice_number": "INV-001"
  }
}
```

#### **Retrieve All Invoices**
```json
{
  "message": "Invoices retrieved successfully.",
  "data": [
    {
      "id": 1,
      "invoice_number": "INV-001",
      "buyer_name": "John Doe"
    },
    {
      "id": 2,
      "invoice_number": "INV-002",
      "buyer_name": "Jane Doe"
    }
  ]
}
```

#### **Add a Payment (Success)**
```json
{
  "message": "Payment added successfully.",
  "data": {
    "id": 1,
    "invoice_id": 1,
    "amount_paid": 500.00
  }
}
```

#### **Delete an Invoice (Error: Not Found)**
```json
{
  "error": "Invoice not found."
}
```

