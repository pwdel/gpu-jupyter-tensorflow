import requests

api_map = {
    'baseurl': 'http://192.168.0.201:4000/api/v0/',
    'opts': {
        'totalcount': '/totalcount',
        'details': '/details',
        'headers': '/headers'
    },
    'ubbets': {
        'totalcount': True,
        'details': True,
        'headers': True
    },
    'ubmarkets': {
        'totalcount': True,
        'details': True,
        'headers': True
    },
    'users': {
        'totalcount': True,
        'details': True,
        'headers': True
    },
    'bets': {
        'totalcount': True,
    },
    'markets': {
        'totalcount': True,
    },
}


def get_api_map():
    return api_map


def check_available_endpoint_options(endpoint):
    opts_list = []
    try:
        for key in list(api_map['opts'].keys()):
            if {api_map[endpoint][key]}:
                opts_list.append(key)
    except KeyError:
        pass
            
    return opts_list


def ping_api(endpoint, opts):
    
    apiMap = get_api_map()
    
    # test if endpoint exists in apiMap
    if endpoint in api_map:
        pass
    else:
        raise KeyError("'ubbets' does not exist in api_map!")
    
    baseurl = apiMap['baseurl']
    
    option = apiMap['opts'][opts]
    
    final_url = baseurl + endpoint + '/' + option
    
    response = requests.get(final_url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"API request failed with status code {response.status_code}")