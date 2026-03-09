# Code from Frederick's A3

"""
Represents the universal WorldClock for GuildQuest and tracks time in days, hours, and minutes.

PATTERN #1 - SINGLETON:
WorldClock now implements the Singleton pattern for the universal/global clock instance.
Individual event times are still plain WorldClock objects; only the global clock
accessed via WorldClock.get_instance() is a Singleton.
Lines marked with # [SINGLETON] were added or changed for this pattern.
"""


class WorldClock:
    _instance = None  # [SINGLETON] single shared instance for the global clock

    def __init__(self, days=0, hours=0, minutes=0):
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self._normalize()

    @classmethod
    def get_instance(cls):  # [SINGLETON] factory method returning the shared global clock
        """return the single universal clock instance, creating it if needed."""
        if cls._instance is None:
            cls._instance = cls(1, 8, 0)  # [SINGLETON] starts at Day 1, 08:00
        return cls._instance

    @classmethod
    def reset_instance(cls):  # [SINGLETON] used for testing / re-initialisation only
        """reset the singleton (testing/re-init use only)."""
        cls._instance = None

    def get_days(self):
        return self.days

    def get_hours(self):
        return self.hours

    def get_minutes(self):
        return self.minutes

    def advance(self, days, hours, minutes):
        """advance time by specified amounts."""
        self.days += days
        self.hours += hours
        self.minutes += minutes
        self._normalize()

    def _normalize(self):
        """normalise time values so minutes < 60 and hours < 24."""
        if self.minutes >= 60:
            self.hours += self.minutes // 60
            self.minutes = self.minutes % 60
        if self.hours >= 24:
            self.days += self.hours // 24
            self.hours = self.hours % 24

    def apply_offset(self, offset_hours):
        """apply realm time offset to get local time."""
        local = WorldClock(self.days, self.hours, self.minutes)
        local.hours += offset_hours
        local._normalize()
        return local

    def to_minutes(self):
        """convert to total minutes for comparison."""
        return self.days * 24 * 60 + self.hours * 60 + self.minutes

    def copy(self):
        """create a copy of this WorldClock (used for event start/end times)."""
        return WorldClock(self.days, self.hours, self.minutes)

    def __str__(self):
        return f"Day {self.days}, {self.hours:02d}:{self.minutes:02d}"
