from collections.abc import Generator
from duration import Duration
from models import Flight

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

    def format_flight(self, flight: Flight):
        itineraries = flight.itineraries
        for itinerary in itineraries:
            self.write_break()
            self.write_blank_line()
            total_duration = Duration.from_pt_string(itinerary.duration)
            segments = itinerary.segments
            accumulated_spaces = 0
            self.write_to_output(f"o DEPART {segments[0].departure.iata_code} (TIME)")
            for segment in segments:
                segment_duration = Duration.from_pt_string(segment.duration)
                dash_length = max(2, (DURATION_ARROW_TOTAL_LENGTH * int(segment_duration.to_minutes()) // int(total_duration.to_minutes())) // 2)
                duration_string = f" {str(segment_duration)} "
                dashed_line = ("-" * dash_length) + duration_string + ("-" * dash_length) + "o"
                preceding_line = "\n" + (" " * accumulated_spaces) + "|"
                accumulated_spaces += len(dashed_line)
                self.write_to_output((preceding_line * 2) + f"{dashed_line} {segment.arrival.iata_code} ({str(segment.duration)})")
            self.write_to_output(f" - ARRIVE ({segments[-1].arrival.at})")
            self.write_blank_line()

    def get_output(self) -> str:
        return self.output

# =========================================================================
#
# o DEPART LAS (TIME)
# |
# |---- 45m ----o LAX
#               |
#               Layover (2h 15m)
#               |
#               |----------- 11h 35m -----------o ARRIVE NRT (TIME)
#
# =========================================================================
