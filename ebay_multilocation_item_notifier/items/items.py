from ebay_multilocation_item_notifier.ebay_search_base import EbaySearchItemBase


class DysonVaccumCleaner(EbaySearchItemBase):
    search_keyword = 'dyson -(ball, dryer, parts, play, spares, toy)'
    search_filters = [
        {'name': 'MaxPrice', 'value': 80}
    ]


class Brompton(EbaySearchItemBase):
    search_keyword = "brompton"


class FoldingBike(EbaySearchItemBase):
    search_keyword = "folding (bike, bicycle) -(exercise, motor, quad, rack)"


class BikeTrailer(EbaySearchItemBase):
    search_keyword = "(bike, cycle) trailer"
    search_filters = [
        {'name': 'MaxPrice', 'value': 25}
    ]


class SackTruck(EbaySearchItemBase):
    search_keyword = "sack truck -(antique, vintage, wooden)"
    search_filters = [
        {'name': 'MaxPrice', 'value': 20}
    ]


class VintageRadio(EbaySearchItemBase):
    search_keyword = "radio (roberts, vintage) -(magazines, times, car, valve, valves)"
    search_filters = [
        {'name': 'MaxPrice', 'value': 10}
    ]

class Headphones(EbaySearchItemBase):
    search_keyword = "(headphones, earphones)"
    search_filters = [
        {'name': 'MaxPrice', 'value': 10}
    ]


class BackpackingTent(EbaySearchItemBase):
    search_keyword = "(back pack, back packer, back packers, back packing, backpack, backpacker, backpackers, backpacking, hiking) tent"
    search_filters = [
        {'name': 'MaxPrice', 'value': 40}
    ]


class Bike(EbaySearchItemBase):
    search_keyword = "(bike, bicycle) -(boys, childs, exercise, girls, journal, kids, magazine, motor, quad, rack)"
    search_filters = [
        {'name': 'MaxPrice', 'value': 15}
    ]
