# -*- coding: utf-8 -*-
import json
import time


def lambda_handler(event, context):
    event[0]['serversideTimestamp'] = round(time.time() * 1000)

    print event
    return event
