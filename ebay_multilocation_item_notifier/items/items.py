import os
from ebay_multilocation_item_notifier.ebay_search_base import EbaySearchItemBase


class EbayPlymouthToBristolSearch(EbaySearchItemBase):
    """Base class, where the subclass represents one item search."""
    default_search_radius = 5
    search_filters = [
        {'name': 'Condition',
         'value': 'Used'},
        {'name': 'ListingType',
         'value': 'Auction'},
        # {'name': 'MaxDistance',
        #  'value': '5'},
        {'name': 'LocalPickupOnly',
         'value': True},
        # Params for searching for sold items:
        # {'name': 'SoldItemsOnly',
        #  'value': True}
    ]
    search_keyword = ""
    search_locations = [
        #  (Location name, UK location postcode, search radius in miles (optional))
        ('Saltash', 'PL12 4EB'),
        ('St Germans', 'PL12 5LS'),
        ('Liskeard', 'PL14 4DX'),
        ('Bodmin Parkway', 'PL30 4BB'),

        ('St Keyne Wishing Well Halt', 'PL14 4SE'),
        ('Causeland', 'PL14 4ST'),
        ('Sandplace', 'PL13 1PJ'),
        ('Looe', 'PL13 1HN'),

        ('Gunnislake', 'PL18 9DZ'),
        ('Calstock', 'PL18 9QY'),
        ('Bere Alston', 'PL20 7EP'),
        ('Bere Ferrers', 'PL20 7JS'),

        ('Tavistock', 'PL19 8AY'),

        ('Office', os.environ['OFFICE_POSTCODE'], 20),
        ('Plymouth', 'PL4 6AB', 20),
        ('Ivybridge', 'PL21 0DQ'),
        ('Totnes', 'TQ9 5JR'),
        ('Newton Abbot', 'TQ12 2JE'),
        ('Teignmouth', 'TQ14 8PG'),
        ('Dawlish', 'EX7 9PJ'),
        ('Dawlish Warren', 'EX7 0NF'),
        ('Starcross', 'EX6 8PA'),
        ('Exeter St Thomas', 'EX4 1AJ'),
        ('Exeter St Davids', 'EX4 4NT', 20),
        ('Tiverton Parkway', 'EX16 7EH'),
        ('Taunton', 'TA1 1QP'),
        ('Bridgwater', 'TA6 5HB'),
        ('Highbridge & Burnham', 'TA9 3BT'),
        ('Weston-super-Mare', 'BS23 1XY'),
        ('Weston Milton', 'BS22 8PF'),
        ('Worle', 'BS22 6WA'),
        ('Yatton', 'BS49 4AJ'),
        ('Nailsea & Backwell', 'BS48 3LH'),
        ('Parson Street', 'BS3 5PU'),
        ('Bedminster', 'BS3 4LU'),
        ('Bristol Temple Meads', 'BS1 6QF', 20),
        ('Home', os.environ['HOME_POSTCODE'], 20)
    ]


class DysonVaccumCleaner(EbayPlymouthToBristolSearch):
    search_keyword = 'dyson -(ball, dryer, parts, play, spares, toy)'
    search_filters = [
        {'name': 'MaxPrice', 'value': 80}
    ]


class Brompton(EbayPlymouthToBristolSearch):
    search_keyword = "brompton"


class FoldingBike(EbayPlymouthToBristolSearch):
    search_keyword = "folding (bike, bicycle) -(exercise, motor, quad, rack)"


class BikeTrailer(EbayPlymouthToBristolSearch):
    search_keyword = "(bike, cycle) trailer"
    search_filters = [
        {'name': 'MaxPrice', 'value': 25}
    ]


class SackTruck(EbayPlymouthToBristolSearch):
    search_keyword = "sack truck -(antique, vintage, wooden)"
    search_filters = [
        {'name': 'MaxPrice', 'value': 20}
    ]


class VintageRadio(EbayPlymouthToBristolSearch):
    search_keyword = "radio (roberts, vintage) -(magazines, times, car, valve, valves)"
    search_filters = [
        {'name': 'MaxPrice', 'value': 10}
    ]

class Headphones(EbayPlymouthToBristolSearch):
    search_keyword = "(headphones, earphones)"
    search_filters = [
        {'name': 'MaxPrice', 'value': 10}
    ]


class BackpackingTent(EbayPlymouthToBristolSearch):
    search_keyword = "(back pack, back packer, back packers, back packing, backpack, backpacker, backpackers, backpacking, hiking) tent"
    search_filters = [
        {'name': 'MaxPrice', 'value': 40}
    ]


class Bike(EbayPlymouthToBristolSearch):
    search_keyword = "(bike, bicycle) -(boys, childs, exercise, girls, journal, kids, magazine, motor, quad, rack)"
    search_filters = [
        {'name': 'MaxPrice', 'value': 15}
    ]
