from src.common import database

MAILGUN = "mailgun"
mailgun_info = database.Database.find_one(collection=MAILGUN, query={"_id": "1"})

URL = mailgun_info.get("url")
API_KEY = mailgun_info.get("api_key")
FROM = "Web Price Alerts Sandbox {}".format(mailgun_info.get("email"))
SUBJECT = "New price alert on your item {}"
ELAPSED = 600  # 10 minutes or 600 seconds

ITEM_NAME = "item_name"
ITEM_URL = "item_url"
DESIRED_PRICE = "desired_price"
