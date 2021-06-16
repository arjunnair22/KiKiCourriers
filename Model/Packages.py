from dataclasses import dataclass


@dataclass
class Packages(object):
    package_id:int
    package_weight:int
    distance:int
    offer_code:str

    def __lt__(self, other):
        return self.package_weight < other.get('package_weight', 0)