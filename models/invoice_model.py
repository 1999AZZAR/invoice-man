from sqlalchemy import (
    Column, Integer, String, Text, Float, Date, TIMESTAMP, JSON, ForeignKey, func
)
from sqlalchemy.orm import relationship
from models.database_config import Base

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), nullable=False, unique=True)
    buyer_name = Column(String(255), nullable=False)
    buyer_address = Column(Text, nullable=True)
    issue_date = Column(Date, nullable=False)
    order_id = Column(String(50), nullable=True, unique=True)
    items = Column(JSON, nullable=False)  # JSON for storing item details (e.g., [{"item": "Laptop", "qty": 2}])
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    discount = Column(Float, nullable=True, default=0.0)
    shipping_cost = Column(Float, nullable=True, default=0.0)
    outstanding_balance = Column(Float, nullable=True, default=0.0)
    total_amount = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())

    # Relationships
    payments = relationship("Payment", back_populates="invoice")  # One-to-many relationship

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    amount_paid = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method = Column(String(50), nullable=False)
    notes = Column(Text, nullable=True)

    # Back-reference
    invoice = relationship("Invoice", back_populates="payments")
