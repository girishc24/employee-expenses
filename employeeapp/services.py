from django.utils import timezone
from . models import *

def update_subscription_status(subscription):
    current_date = timezone.now().date()
    
    if subscription.end_date < current_date:
        # Current plan is expired, update its status
        subscription.status = "Expired"
        subscription.save()

        # Activate the next queued plan if available
        next_queued_plan = Usersubscription.objects.filter(
            user=subscription.user,
            status="Queued Plan"
        ).order_by('start_date').first()

        if next_queued_plan:
            next_queued_plan.status = "Current Plan"
            next_queued_plan.start_date = current_date
            next_queued_plan.end_date = next_queued_plan.start_date + timezone.timedelta(days=next_queued_plan.sub_plan.duration)
            next_queued_plan.save()

    elif subscription.available == 0:
        # If credits are exhausted, update the status
        subscription.status = "Credits Reached"
        subscription.save()

        # Check if there’s a queued plan to activate
        next_queued_plan = Usersubscription.objects.filter(
            user=subscription.user,
            status="Queued Plan"
        ).order_by('start_date').first()

        if next_queued_plan:
            next_queued_plan.status = "Current Plan"
            next_queued_plan.start_date = current_date
            next_queued_plan.end_date = next_queued_plan.start_date + timezone.timedelta(days=next_queued_plan.sub_plan.duration)
            next_queued_plan.save()

    else:
        # Otherwise, it's still a "Current Plan"
        subscription.status = "Current Plan"
        subscription.save()

def handle_new_subscription(user, new_subscription):
    # Fetch the currently active subscription (if any)
    current_subscription = Usersubscription.objects.filter(
        user=user,
        status="Current Plan"
    ).order_by('-end_date').first()

    if current_subscription:
        # Mark the current plan as "Purchased Plan"
        current_subscription.status = "Queued Plan"
        current_subscription.is_purchased = True
        current_subscription.save()
        
    # Set the new subscription as the current plan
    new_subscription.status = "Current Plan"
    new_subscription.save()
