from flask import Flask, request, jsonify
from models.database_config import SessionLocal, engine, Base
from models.invoice_model import Invoice, Payment
from helpers.db_helper import (
    create_invoice, get_invoices, get_invoice_by_id, update_invoice,
    delete_invoice, add_payment, get_payments
)

app = Flask(__name__)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

@app.route('/invoices', methods=['POST'])
def create_invoice_route():
    db = get_db()
    try:
        data = request.json
        app.logger.info(f"Request data: {data}")

        if not data.get('invoice_number') or not data.get('buyer_name'):
            return jsonify({"error": "Missing required fields"}), 400

        invoice = create_invoice(db, data)
        if not invoice:
            return jsonify({"error": "Failed to create invoice. Possible duplicate invoice number."}), 400

        return jsonify({"message": "Invoice created successfully.", "data": {"id": invoice.id}}), 201
    except Exception as e:
        db.rollback()
        app.logger.error(f"Error while creating invoice: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()

@app.route('/invoices', methods=['GET'])
def get_invoices_route():
    db = get_db()
    try:
        filters = {
            'buyer_name': request.args.get('buyer_name'),
            'issue_date': request.args.get('issue_date'),
        }
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10))
        invoices = get_invoices(db, skip=skip, limit=limit, filters=filters)
        return jsonify({
            'data': [
                {
                    'id': invoice.id,
                    'invoice_number': invoice.invoice_number,
                    'buyer_name': invoice.buyer_name,
                } for invoice in invoices
            ]
        })
    finally:
        db.close()

@app.route('/invoices/all', methods=['GET'])
def get_all_invoices_route():
    db = get_db()
    try:
        invoices = db.query(Invoice).all()
        return jsonify({
            'data': [
                {
                    'id': invoice.id,
                    'invoice_number': invoice.invoice_number,
                    'buyer_name': invoice.buyer_name,
                    'items': invoice.items,
                    'issue_date': invoice.issue_date,
                } for invoice in invoices
            ]
        })
    except Exception as e:
        app.logger.error(f"Error retrieving all invoices: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        db.close()

@app.route('/invoices/<int:invoice_id>', methods=['GET'])
def get_invoice_route(invoice_id):
    db = get_db()
    try:
        invoice = get_invoice_by_id(db, invoice_id)
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        return jsonify({
            'data': {
                'id': invoice.id,
                'invoice_number': invoice.invoice_number,
                'buyer_name': invoice.buyer_name,
                'items': invoice.items,
            }
        })
    finally:
        db.close()

@app.route('/invoices/<int:invoice_id>', methods=['PUT'])
def update_invoice_route(invoice_id):
    db = get_db()
    try:
        update_data = request.json
        invoice = update_invoice(db, invoice_id, update_data)
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        db.commit()
        return jsonify({'message': f'Invoice {invoice_id} updated successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/invoices/<int:invoice_id>', methods=['DELETE'])
def delete_invoice_route(invoice_id):
    db = get_db()
    try:
        result = delete_invoice(db, invoice_id)
        if not result:
            return jsonify({'error': 'Invoice not found'}), 404
        db.commit()
        return jsonify({'message': f'Invoice {invoice_id} deleted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/invoices/<int:invoice_id>/payments', methods=['POST'])
def add_payment_route(invoice_id):
    db = get_db()
    try:
        payment_data = request.json
        payment = add_payment(db, invoice_id, payment_data)
        if not payment:
            return jsonify({'error': 'Failed to add payment'}), 400
        db.commit()
        return jsonify({
            'data': {
                'id': payment.id,
                'invoice_id': payment.invoice_id,
                'amount_paid': payment.amount_paid,
            }
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/invoices/<int:invoice_id>/payments', methods=['GET'])
def get_payments_route(invoice_id):
    db = get_db()
    try:
        payments = get_payments(db, invoice_id)
        if not payments:
            return jsonify({'message': 'No payments found'}), 404
        return jsonify({
            'data': [
                {
                    'id': payment.id,
                    'amount_paid': payment.amount_paid,
                    'payment_date': payment.payment_date,
                    'payment_method': payment.payment_method,
                } for payment in payments
            ]
        })
    finally:
        db.close()

@app.route('/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment_route(payment_id):
    db = get_db()
    try:
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        db.delete(payment)
        db.commit()
        return jsonify({'message': f'Payment {payment_id} deleted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
