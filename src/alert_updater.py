from src.common import database
from src.models.alerts import alert

database.Database.initialize()

alert.check_alerts()
