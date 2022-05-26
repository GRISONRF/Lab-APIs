from flask import Flask, render_template, request

from pprint import pformat
import os
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['TICKETMASTER_KEY']


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/afterparty')
def show_afterparty_form():
    """Show event search form"""

    return render_template('search-form.html')


@app.route('/afterparty/search')
def find_afterparties():
    """Search for afterparties on Eventbrite"""

    keyword = request.args.get('keyword', '')
    postalcode = request.args.get('zipcode', '')
    radius = request.args.get('radius', '')
    unit = request.args.get('unit', '')
    sort = request.args.get('sort', '')

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY,
                'keyword': keyword,
                'postalcode': postalcode,
                'radius': radius,
                'unit': unit,
                'sort': sort
            }

   
    res = requests.get(url, params=payload)  #res is a Response obj.
    #so res.url is the url for the events + my API, so that allows me to extract the data from that website

    data = res.json()  #making all the data into a dictionary

    #events = data['_embedded']['events']   #getting the list os events out of 'data' and storing in a variable.
    #events is a LIST of events.

    #event = events[0] #getting the FIRST event out of the list and storing in a variable

    #event.keys() #getting the keys of this event which is a dict.
    #now we can search the event name, ot dates, etc. by: event['name'] oe event['date']
    
    #params is now igual to whatever the user inputed from the form
    
    # - Use form data from the user to populate any search parameters
    # - Make sure to save the JSON data from the response to the `data`
    #   variable so that it can display on the page. This is useful for
    #   debugging purposes!
    
    # - Replace the empty list in `events` with the list of events from your
    #   search results

    if '_embedded' in data:
        events = data['_embedded']['events']
    else:
        events = []

    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=events)


# ===========================================================================
# FURTHER STUDY
# ===========================================================================


@app.route('/event/<id>')
def get_event_details(id):
    """View the details of an event."""

    # TODO: Finish implementing this view function

    return render_template('event-details.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
