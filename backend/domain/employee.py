class Employee:
    def __init__(self, id: str, name: str, role: str, branch_id: str, is_suspended: bool = False):
        self.id = id
        self.name = name
        self.role = role
        self.branch_id = branch_id
        self.is_suspended = is_suspended

    def assign_branch(self, branch_id: str):
        self.branch_id = branch_id

    def change_role(self, role: str):
        self.role = role

    def suspend(self):
        self.is_suspended = True

    def activate(self):
        self.is_suspended = False
