import scrapy
import json
from..items import ZillowScraperItem

class ZillowSpider(scrapy.Spider):
    name = "zillow"
    start_urls = [
        'https://www.zillow.com/async-create-search-page-state',  # Your base URL
    ]

    current_page = 1

    def start_requests(self):
        url = "https://www.zillow.com/async-create-search-page-state"
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.zillow.com",
            "referer": "https://www.zillow.com/new-york-ny/4_p/",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
        }
        cookies = {
            "zguid": "24|$87f76fa3-5f04-490e-8157-6e1accbe1417",
            "zgsession": "1|3a98be87-1d94-45cc-bcdf-dda8fbd277f5",
        }

        data = {
            "searchQueryState": {
                "mapBounds": {
                    "north": 40.892482071644054,
                    "south": 40.365107572024996,
                    "east": -73.5202374374351,
                    "west": -74.3661847030601
                },
                "filterState": {
                    "sortSelection": {
                        "value": "globalrelevanceex"
                    }
                },
                "usersSearchTerm": "New York, NY",
                "regionSelection": [
                    {
                        "regionId": 6181,
                        "regionType": 2
                    }
                ],
                "pagination": {
                    "currentPage": self.current_page
                }
            },
            "wants": {
                "cat1": ["listResults"],
                "cat2": ["total"]
            }
        }

        yield scrapy.Request(
            url,
            method="PUT",
            headers=headers,
            cookies=cookies,
            body=json.dumps(data),
            callback=self.parse_results
        )

    def parse_results(self, response):
        full_data = json.loads(response.body)
        cat1 = full_data.get("cat1", {})
        list_results = cat1.get("searchResults", {}).get("listResults", [])

        for result in list_results:
            home_info = result.get('hdpData', {}).get('homeInfo', {})
            if home_info:
                item = ZillowScraperItem()  # Create a new item instance
                item['zpid'] = home_info.get("zpid")
                item['streetAddress'] = home_info.get("streetAddress")
                item['zipcode'] = home_info.get("zipcode")
                item['city'] = home_info.get("city")
                item['state'] = home_info.get("state")
                item['latitude'] = home_info.get("latitude")
                item['longitude'] = home_info.get("longitude")
                item['price'] = home_info.get("price")
                item['bathrooms'] = home_info.get("bathrooms")
                item['bedrooms'] = home_info.get("bedrooms")
                item['livingArea'] = home_info.get("livingArea")
                item['homeType'] = home_info.get("homeType")
                item['homeStatus'] = home_info.get("homeStatus")

                yield item  # Yield the item as usual

        # Pagination logic (if any)
        pagination_info = cat1.get("searchList", {}).get("pagination", {})
        if pagination_info.get("nextUrl"):
            self.current_page += 1
            yield scrapy.Request(
                response.url,
                method="PUT",
                headers=response.request.headers,
                cookies=response.request.cookies,
                body=json.dumps({
                    **json.loads(response.request.body),
                    "searchQueryState": {
                        **json.loads(response.request.body).get("searchQueryState", {}),
                        "pagination": {
                            "currentPage": self.current_page
                        }
                    }
                }),
                callback=self.parse_results
            )
