#!/bin/bash

set -e

gcloud functions deploy f_scheduled --entry-point main --runtime python310 --trigger-resource ping_schedule --trigger-event google.pubsub.topic.publish --timeout 540s --region europe-west3 --env-vars-file env-vars.yaml --project allisnotlost


gcloud scheduler jobs delete pubsub_daily --location europe-west3 --project allisnotlost

gcloud scheduler jobs create pubsub pubsub_daily --schedule "0 4 * * *" --topic projects/allisnotlost/topics/ping_schedule --message-body '{"kind": "ping"}' --location europe-west3 --project allisnotlost
