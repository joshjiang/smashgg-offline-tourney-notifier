class SnsTopic(object):
    def __init__(self, sns_topic):
        self._topic = sns_topic
        self._phone = '8287354503'

    def publish_message(self, tournament_data, tournament_link):
        """Get the topic from the AWS account."""
        # Return an error if we don't have topics
        try:
            topics = self._topic.list_topics()
            response = self._topic.publish(
                TopicArn='arn:aws:sns:us-east-1:476815464521:SmashggOfflineTourneyNotifierStack-TournamentTopic664DE0FD-1MLFLG4XAC31M',
                Message=f'smash.gg link: {tournament_link}',
                Subject='New NYC Tournament Added',
                MessageStructure='string',
                MessageAttributes={
                    'tournament': {
                        'DataType': 'String',
                        'StringValue': 'true'
                    }
                })
            return response
        except Exception as e:
            print(e)
            return e
