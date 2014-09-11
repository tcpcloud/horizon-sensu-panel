
import horizon


def get_user_home(user):
    dashboard = None
    if user.is_superuser:
        return horizon.get_dashboard('monitoring')
