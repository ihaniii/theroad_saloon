class Invoice:
    STATES = ["draft", "open", "partially_paid", "paid", "cancelled", "refunded"]

    def __init__(self, id: str, customer_id: str, status: str = "draft"):
        self.id = id
        self.customer_id = customer_id
        self.items = []  # List of tuples (item_name, price)
        self.discount = 0.0
        
        if status not in self.STATES:
            raise ValueError(f"Invalid initial status: {status}")
        self.status = status
        
        self.payments = []  # List of tuples (payment_method, amount)
        self.refunds = []   # List of tuples (reason, amount)

    def transition_to(self, target_status: str):
        if target_status not in self.STATES:
            raise ValueError(f"Target status '{target_status}' is not valid.")
            
        current = self.status
        
        # Valid transition checks
        if target_status == "open":
            if current != "draft":
                raise ValueError(f"Cannot open invoice from '{current}'")
        elif target_status == "partially_paid":
            if current not in ["open", "partially_paid"]:
                raise ValueError(f"Cannot register partial payment on '{current}'")
        elif target_status == "paid":
            if current not in ["open", "partially_paid"]:
                raise ValueError(f"Cannot complete payment on '{current}'")
        elif target_status == "cancelled":
            if current not in ["draft", "open"]:
                raise ValueError(f"Cannot cancel invoice when it is '{current}'")
        elif target_status == "refunded":
            if current not in ["partially_paid", "paid"]:
                raise ValueError(f"Cannot refund invoice when it is '{current}'")
                
        self.status = target_status

    def add_item(self, name: str, price: float):
        if self.status not in ["draft", "open"]:
            raise ValueError("Cannot modify items on a closed/paid invoice.")
        if price < 0:
            raise ValueError("Item price cannot be negative.")
        self.items.append((name, price))

    def remove_item(self, name: str):
        if self.status not in ["draft", "open"]:
            raise ValueError("Cannot modify items on a closed/paid invoice.")
        self.items = [item for item in self.items if item[0] != name]

    def apply_discount(self, rate: float):
        if self.status not in ["draft", "open"]:
            raise ValueError("Cannot apply discount on a closed/paid invoice.")
        if not (0.0 <= rate <= 1.0):
            raise ValueError("Discount rate must be between 0.0 and 1.0.")
        self.discount = rate

    def get_total(self) -> float:
        subtotal = sum(item[1] for item in self.items)
        total = subtotal * (1.0 - self.discount)
        return max(0.0, total)

    def get_total_paid(self) -> float:
        return sum(payment[1] for payment in self.payments)

    def get_total_refunded(self) -> float:
        return sum(refund[1] for refund in self.refunds)

    def register_payment(self, method: str, amount: float):
        if self.status == "draft":
            self.transition_to("open")
        if self.status not in ["open", "partially_paid"]:
            raise ValueError("Invoice is not open for payments.")
        if amount <= 0:
            raise ValueError("Payment amount must be positive.")
            
        self.payments.append((method, amount))
        total_paid = self.get_total_paid()
        total_due = self.get_total()
        
        if total_paid >= total_due:
            self.transition_to("paid")
        else:
            self.transition_to("partially_paid")

    def issue_refund(self, reason: str, amount: float):
        total_paid = self.get_total_paid()
        total_refunded = self.get_total_refunded()
        
        if amount <= 0:
            raise ValueError("Refund amount must be positive.")
        if total_refunded + amount > total_paid:
            raise ValueError("Refund amount cannot exceed total paid amount.")
            
        if self.status not in ["partially_paid", "paid", "refunded"]:
            self.transition_to("refunded")
            
        self.refunds.append((reason, amount))
        
        if self.get_total_refunded() >= total_paid:
            self.status = "refunded"
