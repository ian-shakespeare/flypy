from typing import Generator
from amadeus import Client, Response, ResponseError
from models import Flight

class Flights:
    def __init__(self, key: str, secret: str):
        self.client = Client(client_id=key, client_secret=secret)
        return

    def get_flights(
            self,
            origin_code: str,
            destination_code: str,
            departure_date: str) -> Generator[Flight, None, None]:
        try:
            response: Response = self.client.shopping.flight_offers_search.get(
                    originLocationCode=origin_code,
                    destinationLocationCode=destination_code,
                    departureDate=departure_date,
                    adults=1)
            if response.data is None:
                return
            for data in response.data:
                yield Flight.from_dict(data)
        except ResponseError as error:
            print(error)
            return
