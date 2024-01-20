from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Aircraft:
    code: str

    @staticmethod
    def from_dict(obj: Any) -> 'Aircraft':
        assert isinstance(obj, dict)
        code = from_str(obj.get("code"))
        return Aircraft(code)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = from_str(self.code)
        return result


@dataclass
class Arrival:
    iata_code: str
    at: str
    terminal: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Arrival':
        assert isinstance(obj, dict)
        iata_code = from_str(obj.get("iataCode"))
        at = from_str(obj.get("at"))
        terminal = from_union([from_str, from_none], obj.get("terminal"))
        return Arrival(iata_code, at, terminal)

    def to_dict(self) -> dict:
        result: dict = {}
        result["iataCode"] = from_str(self.iata_code)
        result["at"] = from_str(self.at)
        if self.terminal is not None:
            result["terminal"] = from_union([from_str, from_none], self.terminal)
        return result


@dataclass
class Operating:
    carrier_code: str

    @staticmethod
    def from_dict(obj: Any) -> 'Operating':
        assert isinstance(obj, dict)
        carrier_code = from_str(obj.get("carrierCode"))
        return Operating(carrier_code)

    def to_dict(self) -> dict:
        result: dict = {}
        result["carrierCode"] = from_str(self.carrier_code)
        return result


@dataclass
class Stop:
    iata_code: str
    duration: str
    arrival_at: str
    departure_at: str

    @staticmethod
    def from_dict(obj: Any) -> 'Stop':
        assert isinstance(obj, dict)
        iata_code = from_str(obj.get("iataCode"))
        duration = from_str(obj.get("duration"))
        arrival_at = from_str(obj.get("arrivalAt"))
        departure_at = from_str(obj.get("departureAt"))
        return Stop(iata_code, duration, arrival_at, departure_at)

    def to_dict(self) -> dict:
        result: dict = {}
        result["iataCode"] = from_str(self.iata_code)
        result["duration"] = from_str(self.duration)
        result["arrivalAt"] = from_str(self.arrival_at)
        result["departureAt"] = from_str(self.departure_at)
        return result


@dataclass
class Segment:
    departure: Arrival
    arrival: Arrival
    carrier_code: str
    number: str
    aircraft: Aircraft
    operating: Operating
    duration: str
    id: str
    number_of_stops: int
    blacklisted_in_eu: bool
    stops: Optional[List[Stop]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Segment':
        assert isinstance(obj, dict)
        departure = Arrival.from_dict(obj.get("departure"))
        arrival = Arrival.from_dict(obj.get("arrival"))
        carrier_code = from_str(obj.get("carrierCode"))
        number = from_str(obj.get("number"))
        aircraft = Aircraft.from_dict(obj.get("aircraft"))
        operating = Operating.from_dict(obj.get("operating"))
        duration = from_str(obj.get("duration"))
        id = from_str(obj.get("id"))
        number_of_stops = from_int(obj.get("numberOfStops"))
        blacklisted_in_eu = from_bool(obj.get("blacklistedInEU"))
        stops = from_union([lambda x: from_list(Stop.from_dict, x), from_none], obj.get("stops"))
        return Segment(departure, arrival, carrier_code, number, aircraft, operating, duration, id, number_of_stops, blacklisted_in_eu, stops)

    def to_dict(self) -> dict:
        result: dict = {}
        result["departure"] = to_class(Arrival, self.departure)
        result["arrival"] = to_class(Arrival, self.arrival)
        result["carrierCode"] = from_str(self.carrier_code)
        result["number"] = from_str(self.number)
        result["aircraft"] = to_class(Aircraft, self.aircraft)
        result["operating"] = to_class(Operating, self.operating)
        result["duration"] = from_str(self.duration)
        result["id"] = from_str(self.id)
        result["numberOfStops"] = from_int(self.number_of_stops)
        result["blacklistedInEU"] = from_bool(self.blacklisted_in_eu)
        if self.stops is not None:
            result["stops"] = from_union([lambda x: from_list(lambda x: to_class(Stop, x), x), from_none], self.stops)
        return result


@dataclass
class Itinerary:
    duration: str
    segments: List[Segment]

    @staticmethod
    def from_dict(obj: Any) -> 'Itinerary':
        assert isinstance(obj, dict)
        duration = from_str(obj.get("duration"))
        segments = from_list(Segment.from_dict, obj.get("segments"))
        return Itinerary(duration, segments)

    def to_dict(self) -> dict:
        result: dict = {}
        result["duration"] = from_str(self.duration)
        result["segments"] = from_list(lambda x: to_class(Segment, x), self.segments)
        return result


@dataclass
class Fee:
    amount: str
    type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Fee':
        assert isinstance(obj, dict)
        amount = from_str(obj.get("amount"))
        type = from_str(obj.get("type"))
        return Fee(amount, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["amount"] = from_str(self.amount)
        result["type"] = from_str(self.type)
        return result


@dataclass
class GroupMessagePrice:
    currency: str
    total: str
    base: str
    fees: List[Fee]
    grand_total: str

    @staticmethod
    def from_dict(obj: Any) -> 'GroupMessagePrice':
        assert isinstance(obj, dict)
        currency = from_str(obj.get("currency"))
        total = from_str(obj.get("total"))
        base = from_str(obj.get("base"))
        fees = from_list(Fee.from_dict, obj.get("fees"))
        grand_total = from_str(obj.get("grandTotal"))
        return GroupMessagePrice(currency, total, base, fees, grand_total)

    def to_dict(self) -> dict:
        result: dict = {}
        result["currency"] = from_str(self.currency)
        result["total"] = from_str(self.total)
        result["base"] = from_str(self.base)
        result["fees"] = from_list(lambda x: to_class(Fee, x), self.fees)
        result["grandTotal"] = from_str(self.grand_total)
        return result


@dataclass
class PricingOptions:
    fare_type: List[str]
    included_checked_bags_only: bool

    @staticmethod
    def from_dict(obj: Any) -> 'PricingOptions':
        assert isinstance(obj, dict)
        fare_type = from_list(from_str, obj.get("fareType"))
        included_checked_bags_only = from_bool(obj.get("includedCheckedBagsOnly"))
        return PricingOptions(fare_type, included_checked_bags_only)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fareType"] = from_list(from_str, self.fare_type)
        result["includedCheckedBagsOnly"] = from_bool(self.included_checked_bags_only)
        return result


@dataclass
class AmenityProvider:
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'AmenityProvider':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        return AmenityProvider(name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        return result


@dataclass
class Amenity:
    description: str
    is_chargeable: bool
    amenity_type: str
    amenity_provider: AmenityProvider

    @staticmethod
    def from_dict(obj: Any) -> 'Amenity':
        assert isinstance(obj, dict)
        description = from_str(obj.get("description"))
        is_chargeable = from_bool(obj.get("isChargeable"))
        amenity_type = from_str(obj.get("amenityType"))
        amenity_provider = AmenityProvider.from_dict(obj.get("amenityProvider"))
        return Amenity(description, is_chargeable, amenity_type, amenity_provider)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_str(self.description)
        result["isChargeable"] = from_bool(self.is_chargeable)
        result["amenityType"] = from_str(self.amenity_type)
        result["amenityProvider"] = to_class(AmenityProvider, self.amenity_provider)
        return result


@dataclass
class IncludedCheckedBags:
    quantity: int

    @staticmethod
    def from_dict(obj: Any) -> 'IncludedCheckedBags':
        assert isinstance(obj, dict)
        quantity = from_int(obj.get("quantity"))
        return IncludedCheckedBags(quantity)

    def to_dict(self) -> dict:
        result: dict = {}
        result["quantity"] = from_int(self.quantity)
        return result


@dataclass
class FareDetailsBySegment:
    segment_id: str
    cabin: str
    fare_basis: str
    fare_details_by_segment_class: str
    included_checked_bags: IncludedCheckedBags
    branded_fare: Optional[str] = None
    branded_fare_label: Optional[str] = None
    amenities: Optional[List[Amenity]] = None
    slice_dice_indicator: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FareDetailsBySegment':
        assert isinstance(obj, dict)
        segment_id = from_str(obj.get("segmentId"))
        cabin = from_str(obj.get("cabin"))
        fare_basis = from_str(obj.get("fareBasis"))
        fare_details_by_segment_class = from_str(obj.get("class"))
        included_checked_bags = IncludedCheckedBags.from_dict(obj.get("includedCheckedBags"))
        branded_fare = from_union([from_str, from_none], obj.get("brandedFare"))
        branded_fare_label = from_union([from_str, from_none], obj.get("brandedFareLabel"))
        amenities = from_union([lambda x: from_list(Amenity.from_dict, x), from_none], obj.get("amenities"))
        slice_dice_indicator = from_union([from_str, from_none], obj.get("sliceDiceIndicator"))
        return FareDetailsBySegment(segment_id, cabin, fare_basis, fare_details_by_segment_class, included_checked_bags, branded_fare, branded_fare_label, amenities, slice_dice_indicator)

    def to_dict(self) -> dict:
        result: dict = {}
        result["segmentId"] = from_str(self.segment_id)
        result["cabin"] = from_str(self.cabin)
        result["fareBasis"] = from_str(self.fare_basis)
        result["class"] = from_str(self.fare_details_by_segment_class)
        result["includedCheckedBags"] = to_class(IncludedCheckedBags, self.included_checked_bags)
        if self.branded_fare is not None:
            result["brandedFare"] = from_union([from_str, from_none], self.branded_fare)
        if self.branded_fare_label is not None:
            result["brandedFareLabel"] = from_union([from_str, from_none], self.branded_fare_label)
        if self.amenities is not None:
            result["amenities"] = from_union([lambda x: from_list(lambda x: to_class(Amenity, x), x), from_none], self.amenities)
        if self.slice_dice_indicator is not None:
            result["sliceDiceIndicator"] = from_union([from_str, from_none], self.slice_dice_indicator)
        return result


@dataclass
class TravelerPricingPrice:
    currency: str
    total: str
    base: str

    @staticmethod
    def from_dict(obj: Any) -> 'TravelerPricingPrice':
        assert isinstance(obj, dict)
        currency = from_str(obj.get("currency"))
        total = from_str(obj.get("total"))
        base = from_str(obj.get("base"))
        return TravelerPricingPrice(currency, total, base)

    def to_dict(self) -> dict:
        result: dict = {}
        result["currency"] = from_str(self.currency)
        result["total"] = from_str(self.total)
        result["base"] = from_str(self.base)
        return result


@dataclass
class TravelerPricing:
    traveler_id: str
    fare_option: str
    traveler_type: str
    price: TravelerPricingPrice
    fare_details_by_segment: List[FareDetailsBySegment]

    @staticmethod
    def from_dict(obj: Any) -> 'TravelerPricing':
        assert isinstance(obj, dict)
        traveler_id = from_str(obj.get("travelerId"))
        fare_option = from_str(obj.get("fareOption"))
        traveler_type = from_str(obj.get("travelerType"))
        price = TravelerPricingPrice.from_dict(obj.get("price"))
        fare_details_by_segment = from_list(FareDetailsBySegment.from_dict, obj.get("fareDetailsBySegment"))
        return TravelerPricing(traveler_id, fare_option, traveler_type, price, fare_details_by_segment)

    def to_dict(self) -> dict:
        result: dict = {}
        result["travelerId"] = from_str(self.traveler_id)
        result["fareOption"] = from_str(self.fare_option)
        result["travelerType"] = from_str(self.traveler_type)
        result["price"] = to_class(TravelerPricingPrice, self.price)
        result["fareDetailsBySegment"] = from_list(lambda x: to_class(FareDetailsBySegment, x), self.fare_details_by_segment)
        return result


@dataclass
class Flight:
    type: str
    id: str
    source: str
    instant_ticketing_required: bool
    non_homogeneous: bool
    one_way: bool
    last_ticketing_date: str
    last_ticketing_date_time: str
    number_of_bookable_seats: int
    itineraries: List[Itinerary]
    price: GroupMessagePrice
    pricing_options: PricingOptions
    validating_airline_codes: List[str]
    traveler_pricings: List[TravelerPricing]

    @staticmethod
    def from_dict(obj: Any) -> 'Flight':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        id = from_str(obj.get("id"))
        source = from_str(obj.get("source"))
        instant_ticketing_required = from_bool(obj.get("instantTicketingRequired"))
        non_homogeneous = from_bool(obj.get("nonHomogeneous"))
        one_way = from_bool(obj.get("oneWay"))
        last_ticketing_date = from_str(obj.get("lastTicketingDate"))
        last_ticketing_date_time = from_str(obj.get("lastTicketingDateTime"))
        number_of_bookable_seats = from_int(obj.get("numberOfBookableSeats"))
        itineraries = from_list(Itinerary.from_dict, obj.get("itineraries"))
        price = GroupMessagePrice.from_dict(obj.get("price"))
        pricing_options = PricingOptions.from_dict(obj.get("pricingOptions"))
        validating_airline_codes = from_list(from_str, obj.get("validatingAirlineCodes"))
        traveler_pricings = from_list(TravelerPricing.from_dict, obj.get("travelerPricings"))
        return Flight(type, id, source, instant_ticketing_required, non_homogeneous, one_way, last_ticketing_date, last_ticketing_date_time, number_of_bookable_seats, itineraries, price, pricing_options, validating_airline_codes, traveler_pricings)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["id"] = from_str(self.id)
        result["source"] = from_str(self.source)
        result["instantTicketingRequired"] = from_bool(self.instant_ticketing_required)
        result["nonHomogeneous"] = from_bool(self.non_homogeneous)
        result["oneWay"] = from_bool(self.one_way)
        result["lastTicketingDate"] = from_str(self.last_ticketing_date)
        result["lastTicketingDateTime"] = from_str(self.last_ticketing_date_time)
        result["numberOfBookableSeats"] = from_int(self.number_of_bookable_seats)
        result["itineraries"] = from_list(lambda x: to_class(Itinerary, x), self.itineraries)
        result["price"] = to_class(GroupMessagePrice, self.price)
        result["pricingOptions"] = to_class(PricingOptions, self.pricing_options)
        result["validatingAirlineCodes"] = from_list(from_str, self.validating_airline_codes)
        result["travelerPricings"] = from_list(lambda x: to_class(TravelerPricing, x), self.traveler_pricings)
        return result


def flight_from_dict(s: Any) -> List[Flight]:
    return from_list(Flight.from_dict, s)


def flight_to_dict(x: List[Flight]) -> Any:
    return from_list(lambda x: to_class(Flight, x), x)
