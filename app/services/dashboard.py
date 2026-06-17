from datetime import datetime
from sqlalchemy.orm import Session
from app.models.event import Event
from app.models.registration import Registration

class DashboardService:
    @staticmethod
    def get_dashboard_metrics(db: Session, user_id: int, is_admin: bool) -> dict:
        event_query = db.query(Event)
        reg_query = db.query(Registration)

        if not is_admin:
            event_query = event_query.filter(Event.organizer_id == user_id)
            reg_query = reg_query.join(Event).filter(Event.organizer_id == user_id)

        now = datetime.now()

        total_events = event_query.count()
        upcoming_events_count = event_query.filter(Event.start_date > now).count()
        completed_events_count = event_query.filter(Event.end_date < now).count()

        total_participants = reg_query.filter(Registration.status == "Confirmed").group_by(Registration.user_id).count()

        events = event_query.all()
        event_wise_registration_count = []
        for event in events:
            reg_count = db.query(Registration).filter(
                Registration.event_id == event.id,
                Registration.status == "Confirmed"
            ).count()
            event_wise_registration_count.append({
                "event_id": event.id,
                "event_name": event.name,
                "registration_count": reg_count
            })

        return {
            "total_events": total_events,
            "total_participants": total_participants,
            "upcoming_events_count": upcoming_events_count,
            "completed_events_count": completed_events_count,
            "event_wise_registration_count": event_wise_registration_count
        }

dashboard_service = DashboardService()
