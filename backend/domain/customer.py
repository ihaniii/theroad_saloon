class Customer:
    def __init__(self, id: str, name: str, phone: str, is_active: bool = True,
                 allergies: str = "", preferred_beverage: str = "القهوة العربية",
                 total_visits: int = 0, lifetime_value: float = 0.0,
                 loyalty_points: int = 0, loyalty_tier: str = "عامة"):
        self.id = id
        self.name = name
        self.phone = phone
        self.is_active = is_active
        self.allergies = allergies
        self.preferred_beverage = preferred_beverage
        self.total_visits = total_visits
        self.lifetime_value = lifetime_value
        self.loyalty_points = loyalty_points
        self.loyalty_tier = loyalty_tier

    def update_profile(self, name: str, phone: str, allergies: str = None, preferred_beverage: str = None):
        self.name = name
        self.phone = phone
        if allergies is not None:
            self.allergies = allergies
        if preferred_beverage is not None:
            self.preferred_beverage = preferred_beverage

    def add_visit(self, spend: float):
        self.total_visits += 1
        self.lifetime_value += spend
        # Increment loyalty points (1 point per 1 KWD spend)
        self.loyalty_points += int(spend)
        self.update_loyalty_tier()

    def update_loyalty_tier(self):
        if self.loyalty_points >= 1000:
            self.loyalty_tier = "بلاتينية VIP"
        elif self.loyalty_points >= 500:
            self.loyalty_tier = "ذهبية VIP"
        else:
            self.loyalty_tier = "عامة"

    def archive(self):
        self.is_active = False

    def merge_with(self, other_customer: 'Customer'):
        # Consolidate metrics
        self.total_visits += other_customer.total_visits
        self.lifetime_value += other_customer.lifetime_value
        self.loyalty_points += other_customer.loyalty_points
        
        # Combine allergy statements
        if other_customer.allergies:
            if self.allergies:
                self.allergies = f"{self.allergies} | {other_customer.allergies}"
            else:
                self.allergies = other_customer.allergies
                
        self.update_loyalty_tier()
        
        # Archive duplicate
        other_customer.archive()
        return self
