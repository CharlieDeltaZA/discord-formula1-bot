#!/usr/bin/python3
import datetime
import os
import json
from DiscordWebhook import DiscordWebhook
from F1Calendar import F1Calendar
from GTWorldCalendar import GTWorldCalendar
# from discord_webhook import DiscordWebhook

DO_REQUEST = True
root_dir = os.path.dirname(os.path.realpath(__file__))
GTWORLD_CALENDAR = root_dir + "/GTWorldChEu.2021.ics"
F1_CALENDAR = root_dir + "/formula.1.2021.ics"
# WEBHOOK_URL = open(root_dir + '/webhook_url.conf', 'r').readlines()[0].strip()
webhookUrls = open(root_dir + '/webhook_urls.json')
hooks = json.load(webhookUrls)

items = []
gtwcheu = {
    "webhook": DiscordWebhook(hooks['gtworldcheu']),
    "cal": GTWorldCalendar(GTWORLD_CALENDAR)
}
f1 = {
    "webhook": DiscordWebhook(hooks['f1']),
    "cal": GTWorldCalendar(F1_CALENDAR)
}
items.append(f1)
items.append(gtwcheu)
# cal = F1Calendar(CALENDAR_FILE)
# cal = GTWorldCalendar(CALENDAR_FILE)
dow = datetime.datetime.today().weekday()
output_str = None

for i in items:

    # Monday
    if dow == 0:
        # Custom discord emotes in use here...
        prefix_str = u"<:f1:511528935180468225> Happy Monday! Here is the schedule for the next race weekend: \n\n"
        suffix_str = u"<:ferrari:455426708674445312>"
        events = i['cal'].get_next_race_events()
        output_str = prefix_str + "\n".join(events) + "\n" + suffix_str
    # """
    # Suppose this isn't entirely needed. It can fail silently without pushing a message to DC.
    # Tues, Wed, Or None avail
    # USE ME TO DEBUG IF TRYING TO RUN ON A TUES OR WED!
    # elif dow in (1, 2):
    #    events = "None found"
    #    output_str = "No Events Found!"
    # """
    # Thurs, Fri, Sat, Sun

    elif dow in (3, 4, 5, 6):
        # Custom discord emotes in use here...
        prefix_str = u"<:f1:511528935180468225> Race Weekend! In the next 24 hours: \n"
        suffix_str = u"<:ferrari:455426708674445312>"
        events = i['cal'].get_events_next_24h()
        output_str = prefix_str + "\n".join(events) + "\n" + suffix_str

    if events:
        print("Sending: " + output_str)  # .encode('utf-8'))
        # webhook = DiscordWebhook(url=WEBHOOK_URL, content=output_str)

        if DO_REQUEST:
            # response = webhook.execute()
            # print(WEBHOOK_URL)
            # print(response)
            i['webhook'].send_message(output_str)
