#!/usr/bin/env python

import subprocess
from sendgrid.helpers.mail import *
from sendgrid import *

def sendmail(subject, content, to=['developers@openstate.eu']):
    api_key = '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'
    sg = sendgrid.SendGridAPIClient(apikey=api_key)

    mail = Mail()
    mail.set_from(Email("developers@openstate.eu", "Open State Foundation"))
    mail.set_subject(subject)

    personalization = Personalization()
    for address in to:
        personalization.add_to(Email(address))
    mail.add_personalization(personalization)

    mail.add_content(Content("text/plain", content))

    sg.client.mail.send.post(request_body=mail.get())

ip = subprocess.check_output("dig +short myip.opendns.com @resolver1.opendns.com", shell=True).strip()

sendmail('[DUO API] Restarted', 'This is an automated email notifying you that the DUO API has restarted (or at least the `docker_c-duo-api_1` container) on a machine with public IP address %s' % (ip))
