from sns import SnsTopic
from db import TournamentsTable
from call import call
from smashgg import post
import boto3
import time
import json

table_name = 'tournament-table'
# Use boto3 to get an AWS API object that has methods which let us interact with our DynamoDB table
table_resource = boto3.resource('dynamodb').Table(table_name)
sns_client = boto3.client('sns')

# Use the table/topic resources from our classes
dynamo_client = TournamentsTable(table_resource)
sns_client = SnsTopic(sns_client)

# Check to see if there any new tournaments by seeing if we've already put them in the ddb table


def tournament_exists_in_table(tournament_id):
    try:
        if dynamo_client.get_tournament(id=tournament_id):
            return True
    except Exception as e:
        print(e)
        return (e)
    return False


def notify_for_new_touraments(tournament_data):
    count = 0
    tournament_data = json.loads(tournament_data)
    for tournament in tournament_data['data']['tournaments']['nodes']:
        if tournament_exists_in_table(tournament['id']):
            print(f'Tournament {tournament["name"]} already exists')
            continue
        elif tournament['startAt'] > time.time():
            dynamo_client.insert_tournament(tournament['id'])
            count += 1
            tournament_link = 'https://smash.gg' + tournament['url']
            # Send notification with tournament info
            sns_client.publish_message(tournament['name'], tournament_link)
            call(f"{tournament['name']} at {tournament_link}")
            # Success, put the tournament in the table so we don't notify again
    print(f'Total tournaments sent: {count} ')


def lambda_handler(event, context):
    try:
        tournament_data = post()
        if tournament_data:
            notify_for_new_touraments(tournament_data)
            return 'Success'
        return "POST failed: " + tournament_data
    except Exception as e:
        print(e)
        return e
