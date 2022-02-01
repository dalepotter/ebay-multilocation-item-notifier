import os
from ebay_multilocation_item_notifier.keyword_search import KeywordSearch


class BasicKeywordSearch(KeywordSearch):
    """Base class, where the subclass represents one item search."""
    default_search_radius = 5
    remove_duplicates = True
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


class EbayPlymouthToBristolSearch(BasicKeywordSearch):
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


class EbayBristolToChingfordSearch(BasicKeywordSearch):
    search_locations = [
        #  (Location name, UK location postcode, search radius in miles (optional))
        ('Home', os.environ['HOME_POSTCODE'], 10),

        ("M4 J20", "BS32 4JT"),
        ("M4 J19", "BS16 1SX"),
        ("M4 J18", "BS37 6EJ"),
        ("M4 J17", "SN14 6BF"),
        ("M4 J16", "SN4 8QP"),
        ("M4 J15", "SN4 0ET"),
        ("M4 J14", "RG17 0PU"),
        ("M4 J13", "RG20 8XY"),
        ("M4 J12", "RG7 4TX"),
        ("M4 J11", "RG2 8FT"),
        ("M4 J10", "RG40 5QS"),
        ("M4 J9B", "SL6 4LJ"),
        ("M4 J9A", "SL6 2PJ"),
        ("M4 J9", "SL6 2HY"),
        ("M4 J8", "SL6 2HY"),
        ("M4 J7", "SL1 5LX"),
        ("M4 J6", "SL1 2SZ"),
        ("M4 J5", "SL3 8UG"),

        ("M25 J14", "SL3 0FD"),
        ("M25 J15", "UB7 7HQ"),
        ("M25 J16", "SL0 0NY"),
        ("M25 J17", "WD3 5DJ"),
        ("M25 J18", "WD3 5TQ"),
        ("M25 J19", "WD3 4ND"),
        ("M25 J20", "WD4 8QP"),
        ("M25 J21", "WD5 0SB"),
        ("M25 J21A", "AL2 3ET"),
        ("M25 J22", "AL2 1BX"),
        ("M25 J23", "EN6 3NP"),
        ("M25 J24", "EN6 5ER"),
        ("M25 J25", "EN8 8EZ"),
        ("M25 J26", "EN9 3QY"),

        ("Chingford station", "E4 6AL", 10),
        ("Piccadilly Circus station", "W1J 9HS", 10)
    ]


class EbayBristolToExeterSearch(BasicKeywordSearch):
    search_locations = [
        #  (Location name, UK location postcode, search radius in miles (optional))
        ('Home', os.environ['HOME_POSTCODE'], 10),

        ("M5 J18", "BS11 8DL"),
        ("M5 J19", "BS20 7XG"),
        ("M5 J20", "BS21 6XU"),
        ("M5 J21", "BS22 7SQ"),
        ("M5 J22", "TA9 4HF"),
        ("M5 J23", "TA7 8AF"),
        ("M5 J24", "TA7 0DU"),
        ("M5 J25", "TA1 2PG"),
        ("M5 J26", "TA21 9PL"),
        ("M5 J27", "EX16 7HD"),
        ("M5 J28", "EX15 1NS"),
        ("M5 J29", "EX5 2AQ"),
        ("M5 J30", "EX2 7JJ"),

        ("Exeter St Davids station", "EX4 4NT", 20)
    ]


class NailPuller(EbayBristolToChingfordSearch):
    search_keyword = 'nail puller -crow'


class Morgedal(EbayBristolToChingfordSearch):
    search_keyword = 'morgedal'
    search_filters = [
        {'name': 'MaxPrice', 'value': 50}
    ]


class WallpaperSteamer(EbayBristolToChingfordSearch):
    search_keyword = 'wallpaper (stripper, steamer)'
    search_filters = [
        {'name': 'MaxPrice', 'value': 10}
    ]


class Brompton(EbayBristolToChingfordSearch):
    search_keyword = "brompton"
    search_filters = [
        {'name': 'MaxPrice', 'value': 150}
    ]


class RaleighCameo(EbayBristolToChingfordSearch):
    search_keyword = 'raleigh cameo'


class FoldingBike(EbayBristolToChingfordSearch):
    search_keyword = "folding (bike, bicycle) -(exercise, motor, quad, rack)"
    search_filters = [
        {'name': 'MaxPrice', 'value': 80}
    ]


class UppababyVista(EbayBristolToChingfordSearch):
    search_keyword = '(uppababy, uppa baby, upper baby) vista'


class BikeTrailer(EbayBristolToChingfordSearch):
    search_keyword = "(bike, cycle) trailer"
    search_filters = [
        {'name': 'MaxPrice', 'value': 25}
    ]


class SackTruck(EbayBristolToChingfordSearch):
    search_keyword = "sack truck -(antique, vintage, wooden)"
    search_filters = [
        {'name': 'MaxPrice', 'value': 20}
    ]


class BackpackingTent(EbayBristolToChingfordSearch):
    search_keyword = "(back pack, back packer, back packers, back packing, backpack, backpacker, backpackers, backpacking, hiking) tent"
    search_filters = [
        {'name': 'MaxPrice', 'value': 40}
    ]


class Bike(EbayBristolToChingfordSearch):
    search_keyword = "(bike, bicycle) -(boys, childs, exercise, girls, journal, kids, magazine, motor, quad, rack)"
    search_filters = [
        {'name': 'MaxPrice', 'value': 15}
    ]
