from datetime import timedelta

SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24

class Duration:
    def __init__(self, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0):
        self.total_seconds = seconds
        self.total_seconds += SECONDS_PER_MINUTE * minutes
        self.total_seconds += MINUTES_PER_HOUR * SECONDS_PER_MINUTE * hours
        self.total_seconds += HOURS_PER_DAY * MINUTES_PER_HOUR * SECONDS_PER_MINUTE * days

        self.seconds = self.total_seconds % SECONDS_PER_MINUTE
        self.minutes = (self.total_seconds // SECONDS_PER_MINUTE) % MINUTES_PER_HOUR
        self.hours = (self.total_seconds // (MINUTES_PER_HOUR * SECONDS_PER_MINUTE)) % HOURS_PER_DAY
        self.days = self.total_seconds // (MINUTES_PER_HOUR * SECONDS_PER_MINUTE * HOURS_PER_DAY)

    @staticmethod
    def from_pt_string(s: str):
        times = s.replace("PT", "").replace("H", "-").replace("M", "").split("-")
        hours, minutes = times[0] if times[0] != "" else 0, times[1] if times[1] != "" else 0
        td = timedelta(hours=int(hours), minutes=int(minutes))
        return Duration(seconds=int(td.total_seconds()))

    def __str__(self) -> str:
        # 1d 2h 3m 4s
        times: list[str] = []
        if (self.days >= 1):
            times.append(f"{self.days}d")
        if (self.hours >= 1):
            times.append(f"{self.hours}h")
        if (self.minutes >= 1):
            times.append(f"{self.minutes}m")
        if (self.seconds >= 1):
            times.append(f"{self.seconds}s")
        return " ".join(times)

    def to_minutes(self) -> float:
        return self.total_seconds / SECONDS_PER_MINUTE
