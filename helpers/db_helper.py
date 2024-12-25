from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from models.invoice_model import Invoice, Payment
from datetime import datetime

# Create Invoice
def create_invoice(db: Session, invoice_data: dict):
    try:
        # Convert string date to Date object
        if 'issue_date' in invoice_data and isinstance(invoice_data['issue_date'], str):
            invoice_data['issue_date'] = datetime.strptime(invoice_data['issue_date'], '%Y-%m-%d').date()

        # Convert items to JSON format
        if 'items' in invoice_data and isinstance(invoice_data['items'], str):
            items_list = [item.strip() for item in invoice_data['items'].split(',')]
            invoice_data['items'] = [{"item": item, "qty": invoice_data.get('quantity', 1)} for item in items_list]

        # Calculate amount (quantity * unit_price)
        if 'quantity' in invoice_data and 'unit_price' in invoice_data:
            invoice_data['amount'] = invoice_data['quantity'] * invoice_data['unit_price']

        # Set outstanding balance
        invoice_data['outstanding_balance'] = invoice_data.get('total_amount', 0)

        new_invoice = Invoice(**invoice_data)
        db.add(new_invoice)
        db.commit()
        db.refresh(new_invoice)
        return new_invoice
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Database integrity error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error creating invoice: {str(e)}")

# Get All Invoices with Pagination and Filtering
def get_invoices(db: Session, skip: int = 0, limit: int = 10, filters: dict = None):
    query = db.query(Invoice)
    if filters:
        if "buyer_name" in filters:
            query = query.filter(Invoice.buyer_name.ilike(f"%{filters['buyer_name']}%"))
        if "issue_date" in filters:
            query = query.filter(Invoice.issue_date == filters["issue_date"])
    return query.offset(skip).limit(limit).all()

# Get Single Invoice
def get_invoice_by_id(db: Session, invoice_id: int):
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()

# Update Invoice
def update_invoice(db: Session, invoice_id: int, update_data: dict):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        return None
    for key, value in update_data.items():
        setattr(invoice, key, value)
    db.commit()
    db.refresh(invoice)
    return invoice

# Delete Invoice
def delete_invoice(db: Session, invoice_id: int):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        return None
    db.delete(invoice)
    db.commit()
    return {'message': f'Invoice with ID {invoice_id} deleted.'}

# Add Payment to Invoice
def add_payment(db: Session, invoice_id: int, payment_data: dict):
    try:
        new_payment = Payment(invoice_id=invoice_id, **payment_data)
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        return new_payment
    except IntegrityError:
        db.rollback()
        return None

# Get Payments by Invoice ID
def get_payments(db: Session, invoice_id: int):
    return db.query(Payment).filter(Payment.invoice_id == invoice_id).all()
