import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from backend.infrastructure.repositories.sqlite_appointment import SqliteAppointmentRepository
from backend.infrastructure.repositories.sqlite_customer import SqliteCustomerRepository
from backend.infrastructure.repositories.sqlite_employee import SqliteEmployeeRepository
from backend.infrastructure.repositories.sqlite_inventory import SqliteInventoryRepository
from backend.infrastructure.repositories.sqlite_invoice import SqliteInvoiceRepository
from backend.application.appointment.services import AppointmentApplicationService
from backend.application.customer.services import CustomerApplicationService
from backend.application.employee.services import EmployeeApplicationService
from backend.application.inventory.services import InventoryApplicationService
from backend.application.invoice.services import InvoiceApplicationService
from backend.application.appointment.dto import CreateAppointmentRequest
from backend.application.customer.dto import CreateCustomerRequest
from backend.application.employee.dto import CreateEmployeeRequest
from backend.application.inventory.dto import ReceiveStockRequest
from backend.application.invoice.dto import CreateInvoiceRequest
from backend.infrastructure.auth.jwt_handler import JwtHandler
from backend.infrastructure.logging.structured_log import StructuredLogger

class RestApiHandler(BaseHTTPRequestHandler):

    def _send_response(self, status: int, data: dict):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def _get_auth_role(self) -> str:
        # Extract JWT and return role
        auth_header = self.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return "Anonymous"
        token = auth_header.split(" ")[1]
        try:
            payload = JwtHandler.verify_token(token)
            return payload.get("role", "Anonymous")
        except Exception:
            return "Anonymous"

    def do_POST(self):
        # Generate correlation ID for tracking
        correlation_id = self.headers.get("X-Correlation-ID")
        StructuredLogger.set_correlation_id(correlation_id)
        
        path = urllib.parse.urlparse(self.path).path
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        body = json.loads(post_data.decode('utf-8')) if post_data else {}

        user_role = self._get_auth_role()
        StructuredLogger.info(f"POST request received on {path}", {"role": user_role})

        try:
            # Route: Create Appointment
            if path == "/api/v1/appointments":
                repo = SqliteAppointmentRepository()
                service = AppointmentApplicationService(repo)
                req = CreateAppointmentRequest(
                    id=body["id"],
                    customer_id=body["customer_id"],
                    employee_id=body["employee_id"],
                    time_slot=body["time_slot"],
                    user_role=user_role
                )
                res = service.create_appointment(req)
                return self._send_response(201, {
                    "id": res.id,
                    "customer_id": res.customer_id,
                    "employee_id": res.employee_id,
                    "time_slot": res.time_slot,
                    "status": res.status,
                    "checked_in": res.checked_in
                })

            # Route: Create Customer
            elif path == "/api/v1/customers":
                repo = SqliteCustomerRepository()
                service = CustomerApplicationService(repo)
                req = CreateCustomerRequest(
                    id=body["id"],
                    name=body["name"],
                    phone=body["phone"],
                    user_role=user_role
                )
                res = service.create_customer(req)
                return self._send_response(201, {
                    "id": res.id,
                    "name": res.name,
                    "phone": res.phone,
                    "is_active": res.is_active
                })

            # Route: Receive Stock
            elif path == "/api/v1/inventory/receive":
                repo = SqliteInventoryRepository()
                service = InventoryApplicationService(repo)
                req = ReceiveStockRequest(
                    id=body["id"],
                    product_name=body["product_name"],
                    amount=body["amount"],
                    user_role=user_role
                )
                res = service.receive_stock(req)
                return self._send_response(200, {
                    "id": res.id,
                    "product_name": res.product_name,
                    "quantity": res.quantity
                })

            # Route: Create Invoice
            elif path == "/api/v1/invoices":
                repo = SqliteInvoiceRepository()
                service = InvoiceApplicationService(repo)
                req = CreateInvoiceRequest(
                    id=body["id"],
                    customer_id=body["customer_id"],
                    user_role=user_role
                )
                res = service.create_invoice(req)
                return self._send_response(201, {
                    "id": res.id,
                    "customer_id": res.customer_id,
                    "items": res.items,
                    "discount": res.discount,
                    "total": res.total,
                    "is_paid": res.is_paid,
                    "payment_method": res.payment_method,
                    "refunded": res.refunded
                })

            else:
                return self._send_response(404, {"error": "Not Found", "correlation_id": StructuredLogger.get_correlation_id()})

        except Exception as e:
            StructuredLogger.error(f"Error handling request: {str(e)}")
            # Unified error model response
            return self._send_response(400, {
                "error": str(e),
                "correlation_id": StructuredLogger.get_correlation_id(),
                "type": e.__class__.__name__
            })
        finally:
            StructuredLogger.clear_correlation_id()

def start_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RestApiHandler)
    StructuredLogger.info(f"The Road OS REST API starting on port {port}...")
    httpd.serve_forever()
