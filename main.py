#!venv/bin/python

import argparse
from flights import Flights
from formatter import Formatter

def parse_args():
    parser = argparse.ArgumentParser(
            prog="FlyPy",
            description="CLI Flight Search")
    parser.add_argument("-o", "--origin", action="store", required=True)
    parser.add_argument("-d", "--destination", action="store", required=True)
    parser.add_argument("-D", "--departure_date", action="store", help="YYYY-MM-DD", required=True)
    parser.add_argument("-r", "--return_date", action="store", help="YYYY-MM-DD")
    return parser.parse_args()

def main():
    args = parse_args()
    flights = Flights(key="spiTEbRavGnF76JyI9We529pdEgxigof", secret="27cEeLQ787L0BG58")
    results = flights.get_flights(
            origin_code=args.origin,
            destination_code=args.destination,
            departure_date=args.departure_date)
    print(Formatter(results).get_output())

if __name__ == "__main__":
    main()
