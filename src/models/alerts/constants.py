import os

URL = os.environ.get("mailgun_url")
API_KEY = os.environ.get("mailgun_api_key")
FROM = "Web Price Alerts Sandbox {}".format(os.environ.get("mailgun_email"))
SUBJECT = "New price alert on your item {}"
ELAPSED = 600  # 10 minutes or 600 seconds

ITEM_NAME = "item_name"
ITEM_URL = "item_url"
DESIRED_PRICE = "desired_price"
