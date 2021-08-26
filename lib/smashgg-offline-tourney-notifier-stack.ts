import { DockerImageFunction, DockerImageCode } from '@aws-cdk/aws-lambda';
import * as cdk from '@aws-cdk/core';
import { join } from 'path';
import { Rule, Schedule } from '@aws-cdk/aws-events';
import { LambdaFunction } from '@aws-cdk/aws-events-targets'
import { Duration } from '@aws-cdk/core';
import { AttributeType, Table } from '@aws-cdk/aws-dynamodb';
import { Topic } from '@aws-cdk/aws-sns';
import { PolicyStatement } from '@aws-cdk/aws-iam';
import { SnsDestination } from '@aws-cdk/aws-lambda-destinations';


export class SmashggOfflineTourneyNotifierStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    // Dynamo
    new Table(this, 'TournamentTable', {
      tableName: 'tournament-table',
      partitionKey: { name: 'tournament_id', type: AttributeType.NUMBER }
    })
    // SNS
    const topic = new Topic(this, 'TournamentTopic')

    // Lambda
    const fnGet = new DockerImageFunction(this, 'GetTournaments', {
      code: DockerImageCode.fromImageAsset(join(__dirname, 'tournament-handler')),
      onSuccess: new SnsDestination(topic)
    });
    fnGet.addToRolePolicy(new PolicyStatement({
      actions: [
        "sns:ListTopics",
        "sns:Publish",
        "dynamodb:PutItem",
        "dynamodb:GetItem",],
      resources: ['*']
    }))
    // CloudWatch Events
    new Rule(this, 'ScheduleRule', {
      schedule: Schedule.rate(Duration.minutes(1)),
      targets: [new LambdaFunction(fnGet)],
    });
  }
}
