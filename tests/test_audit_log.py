import unittest
from backend.infrastructure.database.audit_log import AuditLogger
from backend.infrastructure.database.connection import DbConnection

class TestAuditLog(unittest.TestCase):
    def setUp(self):
        # Ensure we use SQLite local memory DB
        self.conn = DbConnection.get_connection()
        AuditLogger.initialize_audit_table()

    def test_log_action_persisted(self):
        AuditLogger.log_action("PERMISSION_CHANGE", "Assigned Role Owner to User A", "Owner")
        
        trail = AuditLogger.get_audit_trail()
        self.assertGreater(len(trail), 0)
        self.assertEqual(trail[0]["action_type"], "PERMISSION_CHANGE")
        self.assertEqual(trail[0]["user_role"], "Owner")

if __name__ == '__main__':
    unittest.main()
