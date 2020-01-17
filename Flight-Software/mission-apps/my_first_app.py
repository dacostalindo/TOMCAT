#!/usr/bin/env python3

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
