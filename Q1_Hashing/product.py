"""Product entity for the pharmacy inventory system"""
from datetime import date
from decimal import Decimal, InvalidOperation

class Product:
    """One pharmacy product (e.g. medicine) in the inventory"""
    def __init__(self, product_id, name, price, stock, category, expiry_date, requires_prescription=False):
        if not isinstance(product_id, int) or product_id < 0:
            raise ValueError("Product ID must be a positive whole number")
        if not name.strip():
            raise ValueError("Product name cannot be empty")

        try:
            price = Decimal(str(price))
        except InvalidOperation:
            raise ValueError("Price must be a number")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("Stock must be a positive whole number")
        if not isinstance(expiry_date, date):
            raise ValueError("Expiry date must be a date")

        self.product_id = product_id
        self.name = name.strip()
        self.price = price.quantize(Decimal("0.01"))
        self.stock = stock
        self.category = category.strip()
        self.expiry_date = expiry_date
        self.requires_prescription = requires_prescription

    def is_expired(self, today=None):
        """Return True if the product is expired"""
        if today is None:
            today = date.today()
        return self.expiry_date < today

    def __str__(self):
        prescription = "Yes" if self.requires_prescription else "No"
        return (f"ID: {self.product_id} | Name: {self.name} | "
                f"Price: RM{self.price} | Stock: {self.stock} | "
                f"Category: {self.category} | Expiry: {self.expiry_date} | "
                f"Prescription: {prescription}")

if __name__ == "__main__":
    p = Product(1042, "Paracetamol 500mg", "5.9", 120, "Painkiller",
                date(2027, 6, 30))
    print(p)
    print("Expired?", p.is_expired())

    print("float:  ", 0.1 + 0.2)
    print("Decimal:", Decimal("0.1") + Decimal("0.2"))

    try:
        Product(1043, "Cough Syrup", "-3", 10, "Cough", date(2027, 1, 1))
    except ValueError as error:
        print("Rejected:", error)