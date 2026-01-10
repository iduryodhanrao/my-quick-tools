from datetime import datetime
import pytz

# ---------------------------------------------------
# OOP Class for Timezone Handling
# ---------------------------------------------------
class CountryTime:
    def __init__(self, country_name, timezone):
        self.country_name = country_name
        self.timezone = timezone

    def get_current_time(self):
        tz = pytz.timezone(self.timezone)
        now = datetime.now(tz)
        return now.strftime("%I:%M:%S %p")   # wall‑clock style (HH:MM:SS AM/PM)

    def get_current_date(self):
        tz = pytz.timezone(self.timezone)
        now = datetime.now(tz)
        return now.strftime("%A, %d %B %Y")