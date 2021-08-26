#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { SmashggOfflineTourneyNotifierStack } from '../lib/smashgg-offline-tourney-notifier-stack';

const app = new cdk.App();
new SmashggOfflineTourneyNotifierStack(app, 'SmashggOfflineTourneyNotifierStack', {
  env:{
    region: "us-east-1",
    account: '476815464521'
  }
});
