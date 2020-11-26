# Discord Formula1 Bot

Originally forked from [jfritz](https://github.com/jfritz/discord-formula1-bot) and updated to work in Python 3, because I had issues when trying to use it as it was.

A simple discord bot to post F1 events using webhooks.

This script is designed to be run every 12 hours.

Mondays -
    Send a message with the full next race weekend
    
    
Thursdays, Fridays, Saturdays, Sundays -
    Send a message with events that will occur in the next 24h (if any)

---
## Setup

You will need a number of pip packages:
```
pip3 install icalendar python-dateutil urllib3
```

Add your discord webhook url to `webhook_url.conf`

Configure a crontab (Example set for 8am/pm):
```
0 8,20 * * * /usr/bin/python3 /path/to/main.py > /path/to/bot.log
```

You may need to edit `main.py` and update the calendar name.

Source calendars from [F1Calendar](https://f1calendar.com/).

You will need to edit all the Race Events to include `- Grand Prix`. For example `Austrian Grand Prix` becomes `Austrian Grand Prix - Grand Prix` - This is due to how the end of the weekend events is determined. Will look into making this more robust, but then the source needs to remain uniform.

## Updates

I will be looking into updating this project to make use of the Discord Webhook package, as well finding a more robust way of using only the output of F1Calendar without having to edit each event to include an extra string.