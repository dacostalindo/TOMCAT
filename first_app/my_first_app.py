#!/usr/bin/env python3
# make sure to enter chmod +x my_first_app.py on the command line when in the application folder to allow access
# Makes sure file to be run like a normal executable, ./my-mission-app.py,
# rather than needing to explicitly call the Python interpreter with python my-mission-app.py

#import pyhton API
import app_api

# making sure the python api can accept non-default config files for testing purposes
import argparse

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--config', '-c')

    args = parser.parse_args()

    if args.config is not None:
        SERVICES = app_api.Services(args.config)
    else:
        SERVICES = app_api.Services()

    # setting up query to send and request the monitor service and making sure it works
    request = ' {ping} '

    try:
        response = SERVICES.query(service="monitor-service", query=request)

        #parse out the result to get our response string
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

    # if monitor is okay and
    try:
        response = SERVICES.query(service="telemetry-service", query=request)
    except Exception as e:
        print("Something went wrong: " + str(e) )
        sys.exit(1)

    # inside 'response' is the data for the specific request which returns success (ok/not) and specific errors
    # in this case it's a mutation request for the database service
    data = response["insert"]
    success = data["success"]
    errors = data["errors"]

    if success == False:
        print("Telemetry insert encountered errors: " + str(errors))
        sys.exit(1)
    else:
        print("Telemetry insert completed successfully")

if __name__ == "__main__":
    main()
