from dataclasses import dataclass
from typing import Dict, List

@dataclass
class DashboardAggregatesResponse:
    today_revenue: float
    current_occupancy_rate: float
    active_stylists_count: int
    customers_in_salon: int
    avg_waiting_time_minutes: int
    outstanding_payments: float
    low_stock_alerts_count: int

@dataclass
class RevenueAnalyticsResponse:
    daily_revenue: float
    weekly_revenue: float
    monthly_revenue: float
    revenue_per_service: Dict[str, float]
    average_ticket_value: float

@dataclass
class CustomerAnalyticsResponse:
    new_customers_count: int
    retention_rate: float
    no_show_rate: float
    cancellation_rate: float
    vip_count: int

@dataclass
class StaffAnalyticsResponse:
    employee_id: str
    completed_appointments: int
    revenue_generated: float
    utilization_rate: float
    projected_commission: float
