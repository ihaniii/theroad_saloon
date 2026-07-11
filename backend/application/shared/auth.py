class PermissionError(Exception):
    pass

class Authorizer:
    # Role-based permissions matrix
    PERMISSIONS = {
        "Owner": ["CreateAppointment", "MoveAppointment", "CancelAppointment", "CompleteAppointment", "AssignEmployee", "CheckInCustomer", "CreateCustomer", "UpdateCustomer", "ArchiveCustomer", "MergeCustomers", "SearchCustomers", "CreateEmployee", "AssignBranch", "ChangeRole", "SuspendEmployee", "ActivateEmployee", "ReceiveStock", "AdjustInventory", "ConsumeInventory", "CreateInvoice", "AddInvoiceItem", "RemoveInvoiceItem", "ApplyDiscount", "RegisterPayment", "IssueRefund", "DeleteBranch"],
        "Manager": ["CreateAppointment", "MoveAppointment", "CancelAppointment", "CompleteAppointment", "AssignEmployee", "CheckInCustomer", "CreateCustomer", "UpdateCustomer", "ArchiveCustomer", "MergeCustomers", "SearchCustomers", "CreateEmployee", "AssignBranch", "ChangeRole", "SuspendEmployee", "ActivateEmployee", "ReceiveStock", "AdjustInventory", "ConsumeInventory", "CreateInvoice", "AddInvoiceItem", "RemoveInvoiceItem", "ApplyDiscount", "RegisterPayment", "IssueRefund"],
        "Reception": ["CreateAppointment", "MoveAppointment", "CancelAppointment", "CompleteAppointment", "AssignEmployee", "CheckInCustomer", "CreateCustomer", "UpdateCustomer", "SearchCustomers", "CreateInvoice", "AddInvoiceItem", "RemoveInvoiceItem", "RegisterPayment"],
        "Cashier": ["CreateInvoice", "AddInvoiceItem", "RemoveInvoiceItem", "ApplyDiscount", "RegisterPayment", "IssueRefund"],
        "Stylist": ["SearchCustomers"],
        "Inventory": ["ReceiveStock", "AdjustInventory", "ConsumeInventory"],
    }

    @staticmethod
    def check_permission(user_role: str, action: str):
        allowed_actions = Authorizer.PERMISSIONS.get(user_role, [])
        if action not in allowed_actions:
            raise PermissionError(f"Role '{user_role}' is not authorized to perform '{action}'.")
