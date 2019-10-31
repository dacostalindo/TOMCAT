#!/usr/bin/env python3
# Author: Manuel Lindo
# Purpose: Checks if your host is able to:
# 1. Query the monitor service
#   a. Monitor service is a hardware service which communicates with the
#   OBC(or local dev enviroment in this case) itself in order to obtain information
#   about current processes running  and the amount of memory both available and
#   generally present on the system
#2. Write to the telemetry database through mutation
#   Schema for the writing operation:
#   mutation {
#    insert(timestamp: Integer, subsystem: String!, parameter: String!, value: String!) {
#        success: Boolean!,
#        errors: String!
#    }
#}


import argparse
import app_api
import sys

def on_boot():

    print("OnBoot logic")

def on_command():

    request = '{ ping }'

    try:
        response = SERVICES.query(service="monitor-service", query=request)

        data = response["ping"]

        if data == "pong":
            print("Successfully pinged monitor service")
            status = "Okay"
        else:
            print("Unexpected monitor service response: %s" % data)
            status = "Unexpected"

    except Exception as e:
        print("Something went wrong: " + str(e))
        status = "Error"

    request = '''
        mutation {
            insert(subsystem: "OBC", parameter: "status", value: "%s") {
                success,
                errors
            }
        }
        ''' % (status)

    try:
        response = SERVICES.query(service="telemetry-service", query=request)
    except Exception as e:
        print("Something went wrong: " + str(e) )
        sys.exit(1)

    data = response["insert"]
    success = data["success"]
    errors = data["errors"]

    if success == False:
        print("Telemetry insert encountered errors: " + str(errors))
        sys.exit(1)
    else:
        print("Telemetry insert completed successfully")

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--run', '-r')
    parser.add_argument('--config', '-c')

    args = parser.parse_args()

    if args.config is not None:
        global SERVICES
        SERVICES = app_api.Services(args.config)
    else:
        SERVICES = app_api.Services()

    if args.run == 'OnBoot':
        on_boot()
    elif args.run == 'OnCommand':
        on_command()
    else:
        print("Unknown run level specified")
        sys.exit(1)

if __name__ == "__main__":
    main()
