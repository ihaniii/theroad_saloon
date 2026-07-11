class PackageLedger:
    def __init__(self, id: str, customer_id: str, package_name: str, total_sessions: int, is_frozen: bool = False):
        self.id = id
        self.customer_id = customer_id
        self.package_name = package_name
        self.total_sessions = total_sessions
        self.remaining_sessions = total_sessions
        self.is_frozen = is_frozen

    def redeem_session(self):
        if self.is_frozen:
            raise ValueError("Cannot redeem sessions on a frozen package.")
        if self.remaining_sessions <= 0:
            raise ValueError("No remaining sessions left to redeem.")
        self.remaining_sessions -= 1

    def freeze(self):
        self.is_frozen = True

    def unfreeze(self):
        self.is_frozen = False
