import configparser
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

import requests
from dateutil import tz

cfg = configparser.ConfigParser()
cfg.read(Path(__file__).with_name('settings.conf'))

from_zone = tz.gettz(cfg['time']['src_timezone'])
to_zone = tz.gettz(cfg['time']['dst_timezone'])

transactions_file = sys.argv[1]


def get_auth_token():
    configured_token = cfg['ghostfolio'].get('auth_bearer', '').strip()
    access_token = cfg['ghostfolio'].get('access_token', '').strip()

    if configured_token.count('.') == 2:
        return configured_token

    anonymous_token = access_token or configured_token

    if not anonymous_token:
        raise RuntimeError('Missing Ghostfolio access token or bearer token in settings.conf')

    response = requests.post(
        cfg['ghostfolio']['server_url'].rstrip('/') + '/api/v1/auth/anonymous',
        json={'accessToken': anonymous_token},
        timeout=30
    )
    response.raise_for_status()
    return response.json()['authToken']


def convert_gmt_to_local(date):
    gmt_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    gmt_date = gmt_date.replace(tzinfo=from_zone)
    local_date = gmt_date.astimezone(to_zone)
    return local_date.isoformat()

def convert_eur_usd(amount, date):
    if amount != "":
        short_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
        r = requests.get('https://api.frankfurter.app/'+ short_date +'?to=USD', timeout=20)
        return float(amount)*r.json()['rates']['USD']
    return 0

with open(transactions_file, "r", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = { 'activities': [] }
    next(csv_file)
    for row in csv_reader:
        line = {
            "accountId": cfg['ghostfolio']['account_id'],
            "currency": cfg['ghostfolio']['currency'],
            "dataSource": cfg['ghostfolio']['data_source'],
            "date": convert_gmt_to_local(row[1]),
            "fee": float(row[7]) if row[7] != "" else 0,
            "quantity": float(row[3]),
            "symbol": cfg['ghostfolio']['symbol'],
            "type": "BUY", #We don't sell, HODL
            "unitPrice": float(row[11])
        }
        data['activities'].append(line)
print(json.dumps(data, indent=2))
auth_token = get_auth_token()
x = requests.post(cfg['ghostfolio']['server_url'] + '/api/v1/import',
     json = data,
     headers = {
         "Authorization" : "Bearer " + auth_token,
         "Content-Type" : "application/json"
         },
     #verify=cfg['ghostfolio']['ssl_self_cert'],
     timeout=30)
if x.status_code == 401:
    raise RuntimeError(
        'Ghostfolio rejected the bearer token. Check that the configured access token is valid for the account.'
    )
print(x.text)
