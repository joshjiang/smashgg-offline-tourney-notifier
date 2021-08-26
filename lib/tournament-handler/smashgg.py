import requests
import os


def post():
    query = '''
    query UpcomingNYCTournaments($perPage: Int, $coordinates: String!, $radius: String!) {
        tournaments(query: {
            perPage: $perPage
                sortBy: "startAt DESC"
            filter: {
            location: {
                distanceFrom: $coordinates,
                distance: $radius
            }
            videogameIds: [
                1
            ]
            upcoming:true
            }
        }) {
            nodes {
            id
            name
            city
            startAt 
            url
            }
        }
    }'''
    variables = '''
        {
            "perPage": 10,
            "coordinates": "40.76440917517144, -73.9914393041107",
            "radius": "10mi"
        }
        '''
    token = os.environ['SMASHGG_AUTH_TOKEN']
    response = requests.post('https://api.smash.gg/gql/alpha',
                             json={'query': query, 'variables': variables},
                             headers={'Authorization': 'Bearer ' + token})
    return response.text
