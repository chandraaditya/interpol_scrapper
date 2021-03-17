# Problem
Manually pick a list from [bad_people_lists.csv](bad_people_lists.csv) and create a Python crawler program to scrape the "source_url" to find all the persons and collect their information. The program only has to work for one of the URLs listed in [bad_people_lists.csv](bad_people_lists.csv).
For sites that contain links to the individual detail pages, the crawler should scrape them as well to find as much information about that person.
For sites that have pagination, the crawler should scrape at least two pages.
The program itself has no input arguments and should save the results as one .json file, similar to the example below.


# Example

        {
            "source_code": "INTERPOL_RN",
            "source_name": "INTERPOL Red Notices",
            "source_url": "https://www.interpol.int/How-we-work/Notices/View-Red-Notices",
            "persons": [
                {
                    "firstname": "ATIKAT",
                    "lastname": "KURBANOVA",
                    "about": {
                        "date_of_birth": "1995-03-29",
                        "place_of_birth": "CHALYAKH VILLAGE, TSUNTIYSK DISTRCIT, Russia",
                        "nationality": "Russia",
                        "gender": "Female"
                    },
                    "other": {}
                }
            ]
        }
        
# Bonus Problem
Take the .json results file and index the data using a local [elasticsearch docker container] (https://hub.docker.com/_/elasticsearch)
Perform search using a person's full name, e.g. "ATIKAT KURBANOVA" and show the matched records via a screenshot.

# Deliverable
- Python Crawler source code
- A .json result file
- (Bonus) Screenshot of the Elasticsearch query/matches