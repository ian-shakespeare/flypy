from collections.abc import Generator
from models import Flight
from datetime import timedelta

SECONDS_IN_MINUTE = 60
DURATION_ARROW_TOTAL_LENGTH = 30
BREAK_LENGTH = 72
BREAK = "\n" + ("=" * BREAK_LENGTH) + "\n"

class Formatter:
    def __init__(self, flights: Generator[Flight, None, None]):
        self.output = ""
        for flight in flights:
            self.format_flight(flight)

    def write_to_output(self, message: str):
        self.output += message

    def write_break(self):
        self.output += BREAK

    def write_blank_line(self):
        self.output += "\n"

    def parse_duration(self, date_string: str) -> int:
        times = date_string.replace("PT", "").replace("H", "-").replace("M", "").split("-")
        hours, minutes = times[0] if times[0] != "" else 0, times[1] if times[1] != "" else 0
        td = timedelta(hours=int(hours), minutes=int(minutes))
        return int(td.total_seconds() / SECONDS_IN_MINUTE)

    def format_time(self, date: str) -> str:
        times = date.replace("PT", "").replace("H", "-").replace("M", "").split("-")
        hours = f"{times[0]}hr{'s' if int(times[0]) > 1 else ''}"
        minutes = f"{times[1]}min{'s' if int(times[1]) > 1 else ''}" if times[1] != "" else None
        if (minutes is None):
            return hours
        return f"{hours} {minutes}"

    def format_flight(self, flight: Flight):
        itineraries = flight.itineraries
        for itinerary in itineraries:
            self.write_break()
            self.write_blank_line()
            total_duration = self.parse_duration(itinerary.duration)
            segments = itinerary.segments
            accumulated_spaces = 0
            self.write_to_output(f"o {segments[0].departure.iata_code} - DEPART ({segments[0].departure.at})")
            for segment in segments:
                segment_duration = self.parse_duration(segment.duration)
                dash_length = (DURATION_ARROW_TOTAL_LENGTH * segment_duration // total_duration)
                current_line = ("-" * dash_length) + "o"
                preceding_line = "\n" + (" " * accumulated_spaces) + "|"
                self.write_to_output((preceding_line * 2) + f"{current_line} {segment.arrival.iata_code} ({self.format_time(segment.duration)})")
                accumulated_spaces += dash_length + 1
            self.write_to_output(f" - ARRIVE ({segments[-1].arrival.at})")
            self.write_blank_line()

    def get_output(self) -> str:
        return self.output
