import csv
import boto3

INPUT_CSV = 'DNS Updates.csv'
ENCODING = 'utf-8-sig'
AWS_KEY_ID = ''
AWS_KEY = ''
REGION = 'ap-southeast-2'


def get_zone_id(host, zone_name_id):
    suffix = '.'.join(host.split('.')[1:])
    return zone_name_id[suffix]


def update_dns(host, ip, zone_id):
    response = client.change_resource_record_sets(
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': host,
                        'ResourceRecords': [
                            {
                                'Value': ip,
                            },
                        ],
                        'TTL': 300,
                        'Type': 'A',
                    },
                },
            ],
        },
        HostedZoneId=zone_id,
    )
    return response


client = boto3.client('route53', region_name=REGION, aws_access_key_id=AWS_KEY_ID,
                      aws_secret_access_key=AWS_KEY)

zones = client.list_hosted_zones()
zone_name_id = {x['Name']: x['Id'].split('/')[-1] for x in zones['HostedZones']}

with open(INPUT_CSV, encoding=ENCODING) as F:
    changes = csv.reader(F)
    for row in changes:
        host, old_ip, new_ip = row
        # Add trailing . to host
        if host[-1] != '.':
            host += '.'
        zone_id = get_zone_id(host, zone_name_id)
        response = update_dns(host, new_ip, zone_id)
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200
