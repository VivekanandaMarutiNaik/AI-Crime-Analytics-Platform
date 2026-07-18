from collections import defaultdict
from datetime import datetime

from sqlalchemy import func

from sqlalchemy.orm import Session

from backend.models.case_master import CaseMaster


def get_predictive_trend(db: Session, district=None):

    
        query = (
            db.query(
                CaseMaster.district,
                func.date_trunc(
                    "month",
                    CaseMaster.crime_datetime
                ).label("month"),
                func.count().label("count")
            )
        )

        if district:
            query = query.filter(
                CaseMaster.district.ilike(f"%{district}%")
            )
        records = (
            query.group_by(
                CaseMaster.district,
                func.date_trunc("month", CaseMaster.crime_datetime)
            )
            .order_by(
                CaseMaster.district,
                func.date_trunc("month", CaseMaster.crime_datetime)
            )
            .all()
        )

        district_history = defaultdict(list)

        for r in records:
            district_history[r.district].append({
                "month": r.month,
                "count": r.count
            })

        results = []

        for district_name, history in district_history.items():

            if len(history) >= 2:
                previous = history[-2]["count"]
                current = history[-1]["count"]
            else:
                previous = history[-1]["count"]
                current = previous

            trend_delta = current - previous

            predicted = max(0, round(current + trend_delta))

            if current == 0:
                growth = 0
            else:
                growth = round(
                    ((predicted - current) / current) * 100,
                    2
                )

            if growth > 5:
                trend = "Increasing"
            elif growth < -5:
                trend = "Decreasing"
            else:
                trend = "Stable"

            confidence = round(
                max(
                    50,
                    100 - abs(trend_delta) * 2
                ),
                2
            )

            results.append({
                "district": district_name,
                "current_month_cases": current,
                "predicted_next_month_cases": predicted,
                "growth_percentage": growth,
                "trend": trend,
                "confidence": confidence
            })

        return results

   