term_search: str    = "sono"
items_per_page: int = 100 # max is 100

api_url: str = "https://api.company-information.service.gov.uk/search/companies?q=" \
                + term_search + "&items_per_page=" + str(items_per_page)

json_file: str = 'data.json'
csv_file: str  = 'data.csv'