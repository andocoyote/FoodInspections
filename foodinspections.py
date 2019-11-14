import requests
import json
import pandas as pd


# Snoqualmie: 98065

# This is a base class from which all specific types of searcher classes will derive
class Searcher:
    def __init(self):
        self.MinSearchStringLength = 1
        self.DefaultSearchTerm = None
        self.FriendlySearchType = None
        self.SearchType = None
    
    # This is the main search function that all derived classes will use
    def SearchFunction(self):
        self.SearchTerm = input('Enter the {0}: '.format(self.FriendlySearchType))
        
        # If the user-supplied search term is less than the minimum length required,
        # use the default term instead
        if len(self.SearchTerm) < self.MinSearchStringLength:
            self.SearchTerm = self.DefaultSearchTerm
        
        return self.SearchTerm


# This class knows who to obtain a zip code for which to search from the user
class ZipCodeSearcher(Searcher):
    def __init__(self):
        super().__init__()
        
        # Gotta use 'self.' to reference the base class's member variables
        self.MinSearchStringLength = 5
        self.DefaultSearchTerm = '98034'
        self.FriendlySearchType = 'zip code'
        self.SearchType = 'zip_code'
        

# This class knows who to obtain a city name for which to search from the user
class CitySearcher(Searcher):
    def __init__(self):
        super().__init__()
        
        # Gotta use 'self.' to reference the base class's member variables
        self.MinSearchStringLength = 1
        self.DefaultSearchTerm = 'kirkland'
        self.FriendlySearchType = 'city name'
        self.SearchType = 'city'
        

# This class knows who to obtain a restaurant name for which to search from the user
class RestaurantSearcher(Searcher):
    def __init__(self):
        super().__init__()
        
        # Gotta use 'self.' to reference the base class's member variables
        self.MinSearchStringLength = 1
        self.DefaultSearchTerm = 'plaza garcia'
        self.FriendlySearchType = 'restaurant name'
        self.SearchType = 'name'


MenuOptions = {'1' : ZipCodeSearcher(), '2' : CitySearcher(), '3' : RestaurantSearcher()}
SearchType = {'1' : 'zip_code', '2' : 'city', '3' : 'name'}


# This method displays a menu for the user to select the kind of search they'd like to perform
def DisplayMenu():
    print('1: Search by zip code')
    print('2: Search by city')
    print('3: Search by restaurant name')
    print('0: Exit')
    selection = input('Make your selection: ')

    return selection


# This method performs the actual search using the King County API:
# Parameters
#   search_type: e.g. zip_code, city, name
#   search_term: e.g. 98034, kirkland, pizza hut
# Returns:
#   Requests.Response object
#   json data from the API call
def GetData(search_type, search_term):
    url = 'https://data.kingcounty.gov/resource/f29f-zza5.json'
    header = {'X-App-Token':'LwAqwxdgdAINxx7I4rJ1PRiVm'}

    start_date = input('Enter the start date (yyyy-mm-dd): ')
    if (len(start_date)) < 10:
        start_date = '2019-01-01'

    # Build the filters dictionary to pass to the API
    filters = {'$limit':'50000'}
    filters[search_type] = search_term.upper()
    filters['$where'] = 'inspection_date > \'' + start_date + 'T00:00:00.000\''

    try:
        # Call the API
        response = requests.get(url, headers=header, stream=True, params=filters)
    
    except requests.exceptions.Timeout:
        print('Error: The call to \'get\' timed out.')
    except requests.exceptions.TooManyRedirects:
        print('Error: The URL resulted in too many redirects.')
    except requests.exceptions.RequestException as e:
        print('Error: Exception occured:\n', e)
        sys.exit(1)

    # Demonstrates iteratively grabbing chucks of the data and printing '.' for a progress bar
    str_data = ''
    for chunk in response.iter_content(chunk_size=10000):
        print('.', end='')
        str_data += chunk.decode()

    json_data = json.loads(str_data)
    
    # Dump statistics
    print('Retrieved info for {0} businesses for search term \'{1}\' starting on {2}.'.format(len(json_data), search_term, start_date)) 
    
    return response, json_data


# This is the main method
if __name__ == "__main__":

    # Get the menu choice from the user
    selection = DisplayMenu()
    
    # Based on the menu choice, obtain the search type and term for which to search
    search_type = SearchType[selection]
    search_term = MenuOptions[selection].SearchFunction()

    # Call King County's food establishment inspection API
    response, json_data = GetData(search_type, search_term)

    print(response.headers)

    # Dump all inspection results
    for item in json_data:
        print('Business name: {0}, Address {1} {2} {3}, Score: {4}, Result: {5}'.format(
            item['name'], item['address'], item['city'], item['zip_code'], item['inspection_score'], item['inspection_result']))
        if 'violation_type' in item:
            print('\tViolation type: ', item['violation_type'])
        if 'violation_description' in item:
            print('\tViolation description: ', item['violation_description'])


# df = pd.DataFrame(json_data)
# df[(df['inspection_result'] == 'Unsatisfactory') | (df['inspection_score'] > '10')]
# df[df['inspection_result'] == 'Unsatisfactory']
# df.sort_values(by=['col1'])
# df2[df2['name'] == 'Viking Sports Bar & Grill']['inspection_score']
# df2 = df.sort_values(by=['inspection_score'], ascending=False)
