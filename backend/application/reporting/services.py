from typing import Dict, List
from backend.application.shared.auth import Authorizer
from backend.application.shared.interfaces import AppointmentRepository, CustomerRepository, InvoiceRepository, InventoryRepository
from backend.application.reporting.dto import (
    DashboardAggregatesResponse,
    RevenueAnalyticsResponse,
    CustomerAnalyticsResponse,
    StaffAnalyticsResponse
)

class ReportingApplicationService:
    def __init__(self, appt_repo: AppointmentRepository, cust_repo: CustomerRepository,
                 invoice_repo: InvoiceRepository, inventory_repo: InventoryRepository):
        self.appt_repo = appt_repo
        self.cust_repo = cust_repo
        self.invoice_repo = invoice_repo
        self.inventory_repo = inventory_repo

    def get_dashboard_aggregates(self, user_role: str) -> DashboardAggregatesResponse:
        # Standardize check
        Authorizer.check_permission(user_role, "SearchCustomers") # minimal viewing power
        
        appts = self.appt_repo.find_all()
        invoices = [self.invoice_repo.find_by_id(appt.id) for appt in appts if self.invoice_repo.find_by_id(appt.id)]
        inventory = self.inventory_repo.find_all()

        # Calculate metrics
        today_revenue = sum(inv.get_total_paid() for inv in invoices if inv.status in ["paid", "partially_paid"])
        active_stylists_count = len(set(appt.employee_id for appt in appts if appt.status == "in_service"))
        customers_in_salon = len([appt for appt in appts if appt.status in ["checked_in", "in_service"]])
        outstanding_payments = sum(inv.get_total() - inv.get_total_paid() for inv in invoices if inv.status not in ["paid", "refunded"])
        low_stock_alerts_count = len([item for item in inventory if item.check_reorder()])
        
        return DashboardAggregatesResponse(
            today_revenue=today_revenue,
            current_occupancy_rate=0.75,  # Staging aggregate mock
            active_stylists_count=max(1, active_stylists_count),
            customers_in_salon=customers_in_salon,
            avg_waiting_time_minutes=8,
            outstanding_payments=outstanding_payments,
            low_stock_alerts_count=low_stock_alerts_count
        )

    def get_revenue_analytics(self, user_role: str) -> RevenueAnalyticsResponse:
        # Require management permission
        Authorizer.check_permission(user_role, "ApplyDiscount") # Manager+
        
        appts = self.appt_repo.find_all()
        invoices = [self.invoice_repo.find_by_id(appt.id) for appt in appts if self.invoice_repo.find_by_id(appt.id)]
        
        daily_rev = sum(inv.get_total_paid() for inv in invoices if inv.status in ["paid", "partially_paid"])
        
        # Calculate revenue per service type
        service_revs = {}
        ticket_count = 0
        ticket_sum = 0.0
        
        for inv in invoices:
            if inv.status in ["paid", "partially_paid"]:
                ticket_count += 1
                ticket_sum += inv.get_total()
                for item in inv.items:
                    name = item[0]
                    price = item[1]
                    service_revs[name] = service_revs.get(name, 0.0) + price
                    
        avg_ticket = ticket_sum / max(1, ticket_count)
        
        return RevenueAnalyticsResponse(
            daily_revenue=daily_rev,
            weekly_revenue=daily_rev * 5.4, # weekly approximation based on day
            monthly_revenue=daily_rev * 22.0,
            revenue_per_service=service_revs,
            average_ticket_value=avg_ticket
        )

    def get_customer_analytics(self, user_role: str) -> CustomerAnalyticsResponse:
        Authorizer.check_permission(user_role, "ApplyDiscount")
        
        appts = self.appt_repo.find_all()
        total_appts = len(appts)
        cancels = len([a for a in appts if a.status == "cancelled"])
        no_shows = len([a for a in appts if a.status == "no_show"])
        
        cancel_rate = cancels / max(1, total_appts)
        no_show_rate = no_shows / max(1, total_appts)
        
        return CustomerAnalyticsResponse(
            new_customers_count=2, # Mock aggregates
            retention_rate=0.84,
            no_show_rate=no_show_rate,
            cancellation_rate=cancel_rate,
            vip_count=2
        )

    def get_staff_performance(self, employee_id: str, user_role: str) -> StaffAnalyticsResponse:
        Authorizer.check_permission(user_role, "ApplyDiscount")
        
        appts = [a for a in self.appt_repo.find_all() if a.employee_id == employee_id]
        invoices = [self.invoice_repo.find_by_id(a.id) for a in appts if self.invoice_repo.find_by_id(a.id)]
        
        completed = len([a for a in appts if a.status == "completed"])
        revenue = sum(inv.get_total_paid() for inv in invoices if inv.status in ["paid", "partially_paid"])
        
        # 10% commission projection standard
        projected_commission = revenue * 0.10
        
        return StaffAnalyticsResponse(
            employee_id=employee_id,
            completed_appointments=completed,
            revenue_generated=revenue,
            utilization_rate=0.68,
            projected_commission=projected_commission
        )
