import datetime

from dateutil import tz
from icalendar import Calendar


class GTWorldCalendar(object):

    # See https://pypi.org/project/icalendar/
    # See also https://icalendar.readthedocs.io/en/latest/usage.html
    def __init__(self, filename):
        self.filename = filename
        self.cal_data = Calendar.from_ical(open(self.filename, 'r').read())
        self.cal_events = []

        for item in self.cal_data.walk():
            if item.name == "VEVENT":
                self.cal_events.append(item)

    def get_events_next_7d(self):
        """
        Returns friendly-strings of events that will begin in the next 24h.
        """
        events = self.get_events(
            upcoming_only=True, filter=self._event_filter_next_7d)
        ret = []
        for e in events:
            ret.append(e[0])

        return ret

    def get_events_next_24h(self):
        """
        Returns friendly-strings of events that will begin in the next 24h.
        """
        events = self.get_events(
            upcoming_only=True, filter=self._event_filter_next_24h)
        ret = []
        for e in events:
            ret.append(e[0])

        return ret

    def get_next_race_events(self):
        """
        Returns friendly-strings of events that will take place in the next race weekend.
        """
        events = self.get_events(upcoming_only=True)
        ret = []
        for e in events:
            ret.append(e[0])

            # The race is the last event in a weekend
            if "race 2" in e[1].lower():
                break
            if "race" in e[1].lower():
                break
        return ret

    def get_next_event(self):
        """
        Returns friendly-string of the next session on the calendar.
        """
        return self.get_events()[0]

    def get_events(self, upcoming_only=True, filter=None):
        """
        Returns a list of strings representing race events.
        :param upcoming_only: True = do not return events that have already begun or finished.
        """
        ret = []

        for item in self.cal_events:
            title, start, end, category = self._get_event_data(item)

            # Ignore past events if desired
            if upcoming_only and start < datetime.datetime.now().replace(tzinfo=tz.tzlocal()):
                continue

            # calculate time difference from now
            # assumes times from calendar have a flat 0 microseconds set.
            # See https://stackoverflow.com/questions/3426870/calculating-time-difference#3427051
            now = datetime.datetime.now().replace(microsecond=0).replace(tzinfo=tz.tzlocal())
            diff = start - now

            if filter and not filter(diff):
                continue

            # print(self._get_event_string(title, diff, start, category))
            ret.append(self._get_event_string(title, diff, start, category))
        return ret

    def _event_filter_next_24h(self, diff):
        """
        Event filter. True if the event occurs in the next 23h:59m:59s
        """
        if diff.days < 1:
            return True
        return False

    def _event_filter_next_7d(self, diff):
        if diff.days < 8:
            return True
        return False

    def _get_event_string(self, title, diff, start, category):
        """
        Return a friendly string for an event given the event's title, time diff, and start time
        """
        # Format string message for next event
        # See http://strftime.org/
        # Original - "%a, %b %d %I:%M %p %Z" = Sun, Nov 25 03:10 PM South Africa Standard Time
        # Modified - "%A, %b %d %H:%M %Z" = Sunday, Nov 25 @ 15:10 South Africa Standard Time
        start_friendly = start.strftime("%A, %b %d @ %H:%M %Z")
        # .encode('utf-8')
        return u":arrow_right: **{}**:\n   - Starts in: **{}**\n   - Starts at: **{}**\n".format(title, diff, start_friendly), category

    def _get_event_data(self, event):
        """
        Return raw event data from a calendar (ics) event
        """
        # read event data
        title = event.get('summary').title()
        start_utc = event.get('dtstart').dt
        end_utc = event.get('dtend').dt
        category = event.get('categories').to_ical().decode()

        # convert to local timezone
        # See https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime-with-python#4771733
        start = start_utc.astimezone(tz.tzlocal())
        end = end_utc.astimezone(tz.tzlocal())

        return [title, start, end, category]
