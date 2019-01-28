import datetime
import argparse
from fluent.sender import FluentSender


SENSOR_TOPIC = "sensors"


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ident",
                        help="Unique identifier of the honeypot.")
    parser.add_argument("-n", "--hostname",
                        help="Hostname of the honeypot.")
    parser.add_argument("-t", "--type",
                        help="Honeypot type.")
    parser.add_argument("-a", "--address",
                        help="IP address of the honeypot.")
    parser.add_argument("--fluent-host", default="fluentbit",
                        help="Hostname of Fluent Bit server")
    parser.add_argument("--fluent-port", type=int, default=24284,
                        help="Port of Fluent Bit server")
    parser.add_argument("--fluent-app", default="stingar",
                        help="Application name for Fluent Bit server")
    parser.add_argument("--tags", help="Comma separated tags for honeypot.")
    args = parser.parse_args()

    dt = datetime.datetime.now()

    data = {"identifier": args.ident,
            "hostname": args.hostname,
            "honeypot": args.type,
            "ip": args.address,
            "created": dt.strftime("%Y/%m/%d %H:%M:%S"),
            "updated": dt.strftime("%Y/%m/%d %H:%M:%S"),
            "tags": args.tags}

    sender = FluentSender(args.fluent_app,
                          host=args.fluent_host,
                          port=args.fluent_port)

    sender.emit(SENSOR_TOPIC, data)
    return 0


if __name__ == "__main__":
    main()
