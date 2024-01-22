import unittest
from typing import Generator
from flypy.formatter import Formatter, BREAK
from flypy.models import Flight


DUMMY_FLIGHTS = [
    Flight.from_dict({
        "type": "flight-offer",
        "id": "1",
        "source": "GDS",
        "instantTicketingRequired": False,
        "nonHomogeneous": False,
        "oneWay": False,
        "lastTicketingDate": "2024-03-09",
        "lastTicketingDateTime": "2024-03-09",
        "numberOfBookableSeats": 9,
        "itineraries": [
          {
            "duration": "PT20H40M",
            "segments": [
              {
                "departure": {
                  "iataCode": "LAX",
                  "terminal": "B",
                  "at": "2024-03-09T22:30:00"
                },
                "arrival": {
                  "iataCode": "MNL",
                  "terminal": "1",
                  "at": "2024-03-11T04:00:00"
                },
                "carrierCode": "PR",
                "number": "103",
                "aircraft": {
                  "code": "773"
                },
                "operating": {
                  "carrierCode": "PR"
                },
                "duration": "PT13H30M",
                "id": "72",
                "numberOfStops": 0,
                "blacklistedInEU": False
              },
              {
                "departure": {
                  "iataCode": "MNL",
                  "terminal": "1",
                  "at": "2024-03-11T06:40:00"
                },
                "arrival": {
                  "iataCode": "NRT",
                  "terminal": "2",
                  "at": "2024-03-11T12:10:00"
                },
                "carrierCode": "PR",
                "number": "428",
                "aircraft": {
                  "code": "321"
                },
                "operating": {
                  "carrierCode": "PR"
                },
                "duration": "PT4H30M",
                "id": "73",
                "numberOfStops": 0,
                "blacklistedInEU": False
              }
            ]
          }
        ],
        "price": {
          "currency": "EUR",
          "total": "644.57",
          "base": "422.00",
          "fees": [
            {
              "amount": "0.00",
              "type": "SUPPLIER"
            },
            {
              "amount": "0.00",
              "type": "TICKETING"
            }
          ],
          "grandTotal": "644.57"
        },
        "pricingOptions": {
          "fareType": [
            "PUBLISHED"
          ],
          "includedCheckedBagsOnly": True
        },
        "validatingAirlineCodes": [
          "PR"
        ],
        "travelerPricings": [
          {
            "travelerId": "1",
            "fareOption": "STANDARD",
            "travelerType": "ADULT",
            "price": {
              "currency": "EUR",
              "total": "644.57",
              "base": "422.00"
            },
            "fareDetailsBySegment": [
              {
                "segmentId": "72",
                "cabin": "ECONOMY",
                "fareBasis": "ELOWBUS",
                "class": "E",
                "includedCheckedBags": {
                  "quantity": 2
                }
              },
              {
                "segmentId": "73",
                "cabin": "ECONOMY",
                "fareBasis": "ELOWBUS",
                "class": "E",
                "includedCheckedBags": {
                  "quantity": 2
                }
              }
            ]
          }
        ]
    }),
]


class TestFormatter(unittest.TestCase):
    def get_flights_generator(self) -> Generator[Flight, None, None]:
        for flight in DUMMY_FLIGHTS:
            yield flight

    def test_formatter_output(self):
        flights = self.get_flights_generator()

        formatter = Formatter(flights)
        output = formatter.get_output()

        assert output == (BREAK + "|---------o MNL\n          |          |---o NRT" + BREAK)


if __name__ == "__main__":
    unittest.main()
