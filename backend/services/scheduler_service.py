from apscheduler.schedulers.background import BackgroundScheduler

from core.config import settings
from db.session import SessionLocal
from models.automation import AutomationLog
from models.purchase_order import PurchaseOrder, PurchaseOrderItem
from models.supplier import Supplier
from services.product_service import get_low_stock_products


class SchedulerService:
    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler(timezone="UTC")
        self._started = False

    def start(self) -> None:
        if self._started:
            return
        self.scheduler.add_job(self._run_low_stock_automation, "cron", hour=settings.low_stock_check_hour_utc, id="low_stock")
        self.scheduler.start()
        self._started = True

    def shutdown(self) -> None:
        if self._started:
            self.scheduler.shutdown(wait=False)
            self._started = False

    def _run_low_stock_automation(self):
        db = SessionLocal()
        try:
            low_stock = get_low_stock_products(db)
            default_supplier = db.query(Supplier).first()
            if default_supplier:
                for product in low_stock:
                    quantity = max((product.threshold * 2) - product.stock, 1)
                    po = PurchaseOrder(supplier_id=default_supplier.id, created_by=1, total_amount=product.price * quantity)
                    po.items = [PurchaseOrderItem(product_id=product.id, quantity=quantity, unit_price=product.price)]
                    db.add(po)
            log = AutomationLog(
                job_name="daily_low_stock_check",
                status="SUCCESS",
                message=f"Processed {len(low_stock)} low-stock products",
            )
            db.add(log)
            db.commit()
        except Exception as exc:  # noqa: BLE001
            db.rollback()
            db.add(AutomationLog(job_name="daily_low_stock_check", status="FAILED", message=str(exc)))
            db.commit()
        finally:
            db.close()


scheduler_service = SchedulerService()
