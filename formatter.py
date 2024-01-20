from collections.abc import Generator
from models import Flight

MINUTES_IN_HOUR = 60
BREAK_LENGTH = 64
DURATION_ARROW_TOTAL_LENGTH = 15

class Formatter:
    def __init__(self, flights: Generator[Flight, None, None]):
        self.output = ""
        for flight in flights:
            self.format_flight(flight)

    def write_to_output(self, message: str):
        self.output += message + "\n"

    def write_break(self):
        self.output += "\n" + ("=" * BREAK_LENGTH) + "\n"

    def parse_duration(self, date_string: str) -> int:
        times = date_string.replace("PT", "").replace("H", "-").replace("M", "").split("-")
        hours, minutes = times[0], times[1]
        if (minutes == ""):
            return int(hours) * MINUTES_IN_HOUR
        return (int(hours) * MINUTES_IN_HOUR) + int(minutes)

    def format_flight(self, flight: Flight):
        itineraries = flight.itineraries
        for itinerary in itineraries:
            self.write_break()
            total_duration = self.parse_duration(itinerary.duration)
            segments = itinerary.segments
            for segment in segments:
                segment_duration = self.parse_duration(segment.duration)
                self.write_to_output("-" * (DURATION_ARROW_TOTAL_LENGTH * segment_duration // total_duration))

    def get_output(self) -> str:
        return self.output
