from dataclasses import dataclass


@dataclass
class Packages(object):
    package_id: int
    package_weight: int
    distance: int
    offer_code: str
    is_scheduled: bool = False
    delivery_time_in_hours: int = 0

    def __lt__(self, other):
        return self.package_weight < other.package_weight