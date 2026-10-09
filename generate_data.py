import json
import random
from datetime import datetime, timedelta, timezone
from faker import Faker

fake = Faker()

EVENT_TYPES = [
    "customer_created",
    "trial_started",
    "subscription_created",
    "subscription_upgraded",
    "subscription_downgraded",
    "payment_failed",
    "subscription_canceled"
]

PLANS = {
    "starter_tier": 29.00,
    "pro_tier": 99.00,
    "enterprise_tier": 299.00
}

COUNTRIES = ["US", "CA", "GB", "DE", "AU", "BR"]

def generate_saas_events(num_records=5000):
    events = []
    start_date = datetime.now(timezone.utc) - timedelta(days=90)

    for _ in range(num_records):
        plan_name = random.choice(list(PLANS.keys()))
        event_type = random.choice(EVENT_TYPES)
        
        payment_status = "failed" if event_type == "payment_failed" else "succeeded"
        
        if event_type in ["subscription_canceled", "payment_failed"]:
            mrr_amount = 0.0
        else:
            mrr_amount = PLANS[plan_name]

        event_time = start_date + timedelta(
            seconds=random.randint(0, 90 * 24 * 3600)
        )

        record = {
            "event_id": f"evt_{fake.hexify(text='^^^^^^^^^^^^')}",
            "timestamp": event_time.isoformat(),
            "customer_id": f"cust_{random.randint(1000, 9999)}",
            "customer_email": fake.email(),
            "country": random.choice(COUNTRIES),
            "event_type": event_type,
            "plan_id": plan_name,
            "mrr_amount": mrr_amount,
            "currency": "USD",
            "payment_status": payment_status
        }
        events.append(record)

    output_filename = "raw_saas_events.json"
    with open(output_filename, "w") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")

if __name__ == "__main__":
    generate_saas_events()
