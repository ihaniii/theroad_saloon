import time
import uuid
from typing import Callable
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.infrastructure.logging.structured_log import StructuredLogger
from backend.infrastructure.configuration.config import AppConfig

# Router imports for CRUD resources
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

app = FastAPI(
    title="The Road Company",
    description="Production-grade API for luxury beauty salon operations in the GCC.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Structured Logging & Correlation ID Middleware
@app.middleware("http")
async def add_structured_logs(request: Request, call_next: Callable) -> Response:
    start_time = time.time()
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    StructuredLogger.set_correlation_id(correlation_id)

    # Auth extraction
    auth_header = request.headers.get("Authorization")
    user_role = "Anonymous"
    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.split(" ")[1]
            payload = JwtHandler.verify_token(token)
            user_role = payload.get("role", "Anonymous")
        except Exception:
            pass

    StructuredLogger.info(f"Incoming Request: {request.method} {request.url.path}", {"role": user_role})

    # Execute request pipeline
    response = await call_next(request)
    
    duration = int((time.time() - start_time) * 1000)
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers["X-Response-Time-Ms"] = str(duration)
    
    StructuredLogger.info(f"Completed Request: {response.status_code} in {duration}ms", {"status_code": response.status_code})
    StructuredLogger.clear_correlation_id()
    return response

# Centralized Exception Handler Middleware
@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    StructuredLogger.error(f"Centralized Exception Captured: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": str(exc),
            "correlation_id": StructuredLogger.get_correlation_id(),
            "type": exc.__class__.__name__
        }
    )

# --- OBSERVABILITY / HEALTH CHECK ENDPOINTS ---
@app.get("/health", tags=["Observability"])
async def get_health():
    return {"status": "healthy", "timestamp": int(time.time())}

@app.get("/ready", tags=["Observability"])
async def get_readiness():
    return {"status": "ready"}

@app.get("/live", tags=["Observability"])
async def get_liveness():
    return {"status": "alive"}

# --- REST API v1 ENDPOINTS ---

@app.post("/api/v1/appointments", status_code=status.HTTP_201_CREATED, tags=["Appointments"])
async def create_appointment(body: dict, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    repo = SqliteAppointmentRepository()
    service = AppointmentApplicationService(repo)
    req = CreateAppointmentRequest(
        id=body["id"],
        customer_id=body["customer_id"],
        employee_id=body["employee_id"],
        time_slot=body["time_slot"],
        start_minute=body["start_minute"],
        duration_minutes=body["duration_minutes"],
        room_id=body.get("room_id", "main_room"),
        chair_id=body.get("chair_id", "chair_1"),
        user_role=user_role,
        clean_buffer=body.get("clean_buffer", 15)
    )
    return service.create_appointment(req)

@app.post("/api/v1/appointments/{id}/check-in", tags=["Appointments"])
async def check_in_appointment(id: str, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    repo = SqliteAppointmentRepository()
    service = AppointmentApplicationService(repo)
    return service.check_in_customer(id, user_role)

@app.post("/api/v1/appointments/{id}/complete", tags=["Appointments"])
async def complete_appointment(id: str, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    repo = SqliteAppointmentRepository()
    service = AppointmentApplicationService(repo)
    return service.complete_appointment(id, user_role)

@app.post("/api/v1/appointments/{id}/cancel", tags=["Appointments"])
async def cancel_appointment(id: str, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    repo = SqliteAppointmentRepository()
    service = AppointmentApplicationService(repo)
    return service.cancel_appointment(id, user_role)

@app.post("/api/v1/appointments/{id}/move", tags=["Appointments"])
async def move_appointment(id: str, body: dict, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    repo = SqliteAppointmentRepository()
    service = AppointmentApplicationService(repo)
    return service.move_appointment(id, body["time_slot"], body["start_minute"], user_role)

@app.post("/api/v1/customers", status_code=status.HTTP_201_CREATED, tags=["Customers"])
async def create_customer(body: dict, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    repo = SqliteCustomerRepository()
    service = CustomerApplicationService(repo)
    req = CreateCustomerRequest(
        id=body["id"],
        name=body["name"],
        phone=body["phone"],
        user_role=user_role,
        allergies=body.get("allergies", ""),
        preferred_beverage=body.get("preferred_beverage", "القهوة العربية")
    )
    return service.create_customer(req)

@app.get("/api/v1/customers", tags=["Customers"])
async def search_customers(q: str, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    repo = SqliteCustomerRepository()
    service = CustomerApplicationService(repo)
    return service.search_customers(q, user_role)

@app.get("/api/v1/customers/{id}", tags=["Customers"])
async def get_customer(id: str, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    repo = SqliteCustomerRepository()
    service = CustomerApplicationService(repo)
    cust = repo.find_by_id(id)
    if not cust:
        return JSONResponse(status_code=404, content={"error": "Customer not found"})
    return service._to_response(cust)

@app.patch("/api/v1/customers/{id}", tags=["Customers"])
async def update_customer(id: str, body: dict, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    repo = SqliteCustomerRepository()
    service = CustomerApplicationService(repo)
    return service.update_customer(
        id=id,
        name=body["name"],
        phone=body["phone"],
        allergies=body.get("allergies"),
        preferred_beverage=body.get("preferred_beverage"),
        user_role=user_role
    )

@app.post("/api/v1/customers/merge", tags=["Customers"])
async def merge_customers(body: dict, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    repo = SqliteCustomerRepository()
    service = CustomerApplicationService(repo)
    return service.merge_customers(
        primary_id=body["primary_id"],
        duplicate_id=body["duplicate_id"],
        user_role=user_role
    )

@app.post("/api/v1/inventory/receive", status_code=status.HTTP_200_OK, tags=["Inventory"])
async def receive_stock(body: dict, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    repo = SqliteInventoryRepository()
    service = InventoryApplicationService(repo)
    req = ReceiveStockRequest(
        id=body["id"],
        product_name=body["product_name"],
        amount=body["amount"],
        user_role=user_role,
        sku=body.get("sku", ""),
        reorder_point=body.get("reorder_point", 5),
        warehouse=body.get("warehouse", "Main Store")
    )
    return service.receive_stock(req)

@app.get("/api/v1/inventory", tags=["Inventory"])
async def get_inventory(request: Request):
    repo = SqliteInventoryRepository()
    return repo.find_all()

@app.post("/api/v1/transfers", tags=["Inventory"])
async def transfer_stock(body: dict, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    repo = SqliteInventoryRepository()
    service = InventoryApplicationService(repo)
    req = TransferStockRequest(
        product_id=body["product_id"],
        source_warehouse=body["source_warehouse"],
        target_warehouse=body["target_warehouse"],
        amount=body["amount"],
        user_role=user_role
    )
    return service.transfer_stock(req)

@app.post("/api/v1/stock-adjustments", tags=["Inventory"])
async def adjust_stock(body: dict, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    repo = SqliteInventoryRepository()
    service = InventoryApplicationService(repo)
    return service.adjust_inventory(
        id=body["product_id"],
        new_qty=body["new_qty"],
        user_role=user_role
    )

@app.post("/api/v1/invoices", status_code=status.HTTP_201_CREATED, tags=["POS"])
async def create_invoice(body: dict, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    repo = SqliteInvoiceRepository()
    service = InvoiceApplicationService(repo)
    req = CreateInvoiceRequest(
        id=body["id"],
        customer_id=body["customer_id"],
        user_role=user_role
    )
    return service.create_invoice(req)

@app.post("/api/v1/payments", tags=["POS"])
async def register_payment(body: dict, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    repo = SqliteInvoiceRepository()
    service = InvoiceApplicationService(repo)
    from backend.application.invoice.dto import RegisterPaymentRequest
    req = RegisterPaymentRequest(
        invoice_id=body["invoice_id"],
        method=body["method"],
        amount=body["amount"],
        user_role=user_role
    )
    return service.register_payment(req)

@app.post("/api/v1/refunds", tags=["POS"])
async def issue_refund(body: dict, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    repo = SqliteInvoiceRepository()
    service = InvoiceApplicationService(repo)
    from backend.application.invoice.dto import IssueRefundRequest
    req = IssueRefundRequest(
        invoice_id=body["invoice_id"],
        reason=body["reason"],
        amount=body["amount"],
        user_role=user_role
    )
    return service.issue_refund(req)

@app.get("/api/v1/dashboard", tags=["Intelligence"])
async def get_dashboard(request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    from backend.application.reporting.services import ReportingApplicationService
    service = ReportingApplicationService(
        SqliteAppointmentRepository(),
        SqliteCustomerRepository(),
        SqliteInvoiceRepository(),
        SqliteInventoryRepository()
    )
    return service.get_dashboard_aggregates(user_role)

@app.get("/api/v1/analytics/revenue", tags=["Intelligence"])
async def get_revenue_analytics(request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    from backend.application.reporting.services import ReportingApplicationService
    service = ReportingApplicationService(
        SqliteAppointmentRepository(),
        SqliteCustomerRepository(),
        SqliteInvoiceRepository(),
        SqliteInventoryRepository()
    )
    return service.get_revenue_analytics(user_role)

@app.get("/api/v1/analytics/customers", tags=["Intelligence"])
async def get_customer_analytics(request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    from backend.application.reporting.services import ReportingApplicationService
    service = ReportingApplicationService(
        SqliteAppointmentRepository(),
        SqliteCustomerRepository(),
        SqliteInvoiceRepository(),
        SqliteInventoryRepository()
    )
    return service.get_customer_analytics(user_role)

@app.get("/api/v1/analytics/staff/{employee_id}", tags=["Intelligence"])
async def get_staff_analytics(employee_id: str, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    from backend.application.reporting.services import ReportingApplicationService
    service = ReportingApplicationService(
        SqliteAppointmentRepository(),
        SqliteCustomerRepository(),
        SqliteInvoiceRepository(),
        SqliteInventoryRepository()
    )
    return service.get_staff_performance(employee_id, user_role)

# Global in-memory automation service instance for routing
from backend.application.automation.services import AutomationApplicationService
automation_service = AutomationApplicationService()

@app.post("/api/v1/automations", status_code=status.HTTP_201_CREATED, tags=["Automation"])
async def create_automation_rule(body: dict, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    from backend.application.automation.dto import CreateWorkflowRequest
    req = CreateWorkflowRequest(
        id=body["id"],
        trigger_event=body["trigger_event"],
        conditions=body["conditions"],
        actions=body["actions"],
        user_role=user_role
    )
    return automation_service.create_rule(req)

@app.get("/api/v1/automations", tags=["Automation"])
async def get_automation_rules(request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    return automation_service.get_rules(user_role)

@app.get("/api/v1/automation-history", tags=["Automation"])
async def get_automation_history(request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    return automation_service.get_history(user_role)

# Global in-memory communication service instance for routing
from backend.application.communication.services import CommunicationApplicationService
communication_service = CommunicationApplicationService(SqliteCustomerRepository())

@app.post("/api/v1/messages/send", tags=["Communication"])
async def send_message(body: dict, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    from backend.application.communication.dto import SendMessageRequest
    req = SendMessageRequest(
        recipient=body["recipient"],
        channel=body["channel"],
        template_name=body["template_name"],
        variables=body["variables"],
        language=body.get("language", "ar"),
        user_role=user_role
    )
    return communication_service.send_message(req)

@app.get("/api/v1/messages", tags=["Communication"])
async def get_messages(request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    return communication_service.get_logs(user_role)

@app.get("/api/v1/campaigns", tags=["Communication"])
async def get_campaigns(request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    return communication_service.get_campaigns(user_role)

@app.post("/api/v1/campaigns", tags=["Communication"])
async def create_campaign(body: dict, request: Request):
    user_role = request.headers.get("X-User-Role", "Anonymous")
    from backend.application.communication.dto import CreateCampaignRequest
    req = CreateCampaignRequest(
        id=body["id"],
        name=body["name"],
        template_name=body["template_name"],
        target_tier=body.get("target_tier", "VIP"),
        user_role=user_role
    )
    return communication_service.create_campaign(req)
