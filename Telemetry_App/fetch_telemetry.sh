#!/bin/bash
# Author: Manuel Lindo
# Purpose: After installing and setting up the local environment and making sure
# the monitor service is running, run this shell script. Make sure you are running
# this from kubos directory so you can start the database serice. This script
# will create data entries. pdate all IP addresses in the tools/default_config.toml file,
# changing them from 127.0.0.1 to 0.0.0.0, so that they are available to your host machine.

cargo run --bin telemetry-service -- -c tools/default_config.toml &

curl 0.0.0.0:8002 -H "Content-Type: application/json" --data "{\"query\":\"mutation {insert(subsystem:\\\"OBC\\\",parameter:\\\"voltage\\\",value:\\\"5.0\\\"){success}}\"}"
curl 0.0.0.0:8002 -H "Content-Type: application/json" --data "{\"query\":\"mutation {insert(subsystem:\\\"eps\\\",parameter:\\\"voltage\\\",value:\\\"5.0\\\"){success}}\"}"
curl 0.0.0.0:8002 -H "Content-Type: application/json" --data "{\"query\":\"mutation {insert(subsystem:\\\"OBC\\\",parameter:\\\"current\\\",value:\\\"0.1\\\"){success}}\"}"
curl 0.0.0.0:8002 -H "Content-Type: application/json" --data "{\"query\":\"mutation {insert(subsystem:\\\"eps\\\",parameter:\\\"current\\\",value:\\\"0.1\\\"){success}}\"}"
curl 0.0.0.0:8002 -H "Content-Type: application/json" --data "{\"query\":\"mutation {insert(subsystem:\\\"gps\\\",parameter:\\\"voltage\\\",value:\\\"3.3\\\"){success}}\"}"

open http://0.0.0.0:8002/graphiql

echo "write this to the GraphQL{
  telemetry(subsystem: \"OBC\") {
    timestamp
    subsystem
    parameter
    value
  }
}"
