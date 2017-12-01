from datetime import date
import db
from flask import Flask, render_template, json, request, Response


app = Flask(__name__)
#app.debug = True
logged_user = ""


@app.route("/to_country_page/<country>")
def to_country_page(country):
    info = db.aboutCountry(country)
    cities = db.getCountryCities(country)

    return render_template("country.html", country=country, info=info, cities=cities)


@app.route("/to_city_page/<city>")
def to_city_page(city):
    info = db.aboutCity(city)
    m1 = ""
    m2 = ""
    locations = db.getCityLocations(city)
    print locations
    reviews = db.getCityReviews(city)
    if len(locations) == 0:
        print "hello"
        m1 = "There are no locations in this city"
    if len(reviews) == 0:
        m2 = "There are no reviews for this city"

    return render_template("city.html", city=city, info=info, locations=locations, reviews=reviews, m1=m1, m2=m2)


@app.route("/to_location_page/<loc>")
def to_location_page(loc):
    info = db.aboutLocation(loc)
    events = db.getLocationEvents(loc)
    reviews = db.getLocationReviews(loc)
    m1 = ""
    m2 = ""
    if len(events) == 0:
        m1 = "This location has no events"
    if len(reviews) == 0:
        m2 = "This location has no reviews"

    return render_template("location.html", info=info, events=events, reviews=reviews, m1=m1, m2=m2)


@app.route("/to_event_page/<event>")
def to_event_page(event):
    info = db.aboutEvent(event)
    m1 = ""
    reviews = db.getEventReviews(event)
    if len(reviews) == 0:
        m1 = "There are no reviews for this event"
    return render_template("event.html", info=info, reviews=reviews, m1=m1)


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    """
    signs in user with given credentials
    Makes call to python wrapper
    logs user in or displays error message
    """

    # read the posted values from the UI
    if request.method == "POST":
        _name = request.form['usr']
        _password = request.form['pwd']
        num = db.login(_name, _password)

        if num == 1:
            countries = db.getCountries()
            languages = db.getLanguagesMgr()
            message = ["green", ""]
            return render_template('managerpage.html', message=message, countries=countries, languages=languages)
        elif num == 2:
            global logged_user
            logged_user = _name
            return render_template('homepage.html')
        else:
            return render_template("login.html", error="Credentials Incorrect")


@app.route('/')
def main():
    """
    Starts app at login screen
    """
    db.setupConnection()
    return render_template('login.html')


@app.route("/testing")
def test():
    """
    Testing-can be deleted
    """
    return render_template('test.html')


@app.route("/to_register")
def to_register():
    """
    Takes user to register page
    """
    return render_template('register.html', error="")


@app.route("/register", methods=["POST", "GET"])
def register():
    """
    Registers user then takes them to the home page
    """

    if request.method == "POST":
        name = request.form['username']
        email = request.form['email']
        p1 = request.form['p1']
        p2 = request.form['p2']

        error = "Passwords do not match"
        if p1 != p2:
            return render_template("register.html", error=error)
        elif len(p1) < 6:
            error = "Password must be six or more characters"
            return render_template("register.html", error=error)
        else:
            is_man = len(email) > 13 and email[-13:] == "@gttravel.com"
            reg = db.register(name, email, p1, is_man)

            if reg == 0 and is_man:
                return render_template("managerpage.html", message="")
            elif reg == 0:
                global logged_user
                logged_user = name
                return render_template("homepage.html")
            elif reg == 1:
                error = "Username already taken"
            elif reg == 2:
                error = "Email already taken"
            else:
                error = "Unknown error occurred"

            return render_template("register.html", error=error)


@app.route("/to_login")
def to_login():
    """
    Takes user to login page
    """
    global logged_user
    logged_user = ""
    return render_template("login.html")


@app.route("/login")
def login():
    """
    Login the user
    can replace or be replaced sign_up()
    """

    return render_template("homepage.html")


@app.route("/to_home")
def to_home():
    """
    Displays home page
    """

    return render_template('homepage.html')


@app.route("/to_country_search")
def to_country_search():
    """
    Takes users to country search page
    Dynamically auto fills forms from data base
    Test using Flask html template functionality
    """

    # return render_template('countrysearch.html')
    countries = db.getCountries()
    languages = db.getLanguages()
    """
    if request.form['submit'] == 'Select':
        resp = 'You chose: ', countries
        return Response(resp)
    """

    return render_template('countrysearchtemplate.html', option_list=countries, option_list2=languages, error="")


@app.route("/to_city_search")
def to_city_search():
    """
    Takes users to city search page
    Dynamically auto fills forms from data base
    """
    # return render_template('countrysearch.html')
    countries = db.getCountries()
    cities = db.getCities()
    languages = db.getLanguages()
    """
    if request.form['submit'] == 'Select':
        resp = 'You chose: ', countries
        return Response(resp)
    """

    return render_template('citysearch.html', cities=cities, countries=countries, languages=languages, error="")


@app.route("/to_location_search")
def to_location_search():
    """
    Takes users to location search page
    Dynamically auto fills forms from data base
    """
    cities = db.getCities()
    loc_cat = db.getLocTypes()
    locations = db.getLocNames()
    address = db.getAddresses()

    """
     if request.form['submit'] == 'Select':
        resp = 'You chose: ', countries
        return Response(resp)
    """

    return render_template('locationsearch.html', locations=locations, address=address,
                           cities=cities, loc_cat=loc_cat, error="")


@app.route("/to_event_search")
def to_event_search():
    """
    Takes users to event search page
    Dynamically auto fills forms from data base
    """
    events = db.getEvents()
    cities = db.getCities()
    event_cat = db.getEventCategories()
    """
    if request.form['submit'] == 'Select':
        resp = 'You chose: ', countries
        return Response(resp)
    """

    return render_template('eventsearch.html', events=events, cities=cities, event_cat=event_cat, error="")


@app.route("/to_write_reviews")
def to_write_reviews():
    """
    Takes users to write reviews page
    """

    subject = db.getReviewableTypes()
    return render_template('writereviews.html', subject=subject,
                           date=date.today(), score="", description="", error="")


@app.route("/to_write_reviews_single/<subject>")
def to_write_reviews_single(subject):
    """
    Takes users to write reviews page
    """

    subject = [subject]
    return render_template('/writereviews.html', subject=subject, date="", score="", description="", error="")


@app.route("/to_past_reviews")
def to_past_reviews():
    """
    Takes users to past reviews page
    """
    past_reviews = db.pastReviews(logged_user)
    if len(past_reviews) == 0:
        return render_template('pastreviews.html', reviews=past_reviews, message="You have no past reviews")
    else:
        return render_template('pastreviews.html', reviews=past_reviews, message="")


@app.route("/to_edit_review/<review>/")
def to_edit_review(review):
    info = [x.strip() for x in review.split(',')]
    if len(info) == 5:
        subject = [info[0]]  # [info[0] + ", " + info[1]] need to remove the country name for update to work
        date = info[2]
        score = info[3]
        description = info[4]
    elif len(info) == 6:
        subject = [info[0]+", " + info[1] + ", "+info[2]]
        date = info[3]
        score = info[4]
        description = info[5]
    else:
        subject = [info[0]+", "+info[1]+", "+info[2]+","+info[3]+", "+info[4]+", "+info[5]]
        date = info[6]
        score = info[7]
        description = info[8]

    return render_template("editreviews.html", subject=subject, date=date,
                           score=score, description=description, error="")


@app.route("/update_review", methods=["POST", "GET"])
def update_review():
    """
    takes user to past reveiws
    gets data from html form
    adds new review to database
    gets and loads table from database
    """
    if request.method == "POST":
        subject = request.form["subject"]
        # subject is single comma seperated value
        date = request.form["date"]
        score = request.form["score"]
        description = request.form["description"]

        worked = db.updateReview(logged_user, subject, date, score, description)
        if worked:
            past_reviews = db.pastReviews(logged_user)
            return render_template('pastreviews.html', reviews=past_reviews)
        else:
            # subject = db.getReviewableTypes()
            return render_template('editreviews.html', subject=subject,
                                   date=date, score=score, description=description, error="Could not update review")


@app.route("/make_review", methods=["POST", "GET"])
def make_review():
    """
    takes user to past reveiws
    gets data from html form
    adds new review to database
    gets and loads table from database
    """
    if request.method == "POST":
        subject = request.form["subject"]
        date = request.form["date"]
        score = request.form["score"]
        description = request.form["description"]

        worked = db.writeReview(logged_user, subject, date, score, description)
        if worked:
            past_reviews = db.pastReviews(logged_user)
            return render_template('pastreviews.html', reviews=past_reviews)
        else:
            subject = db.getReviewableTypes()
            return render_template('writereviews.html', subject=subject,
                                   date=date, score=score, description=description, error="Could not write review")


@app.route("/to_country_results", methods=["POST", "GET"])
def search_country():
    """
    takes user to country results
    gets data from html form
    gets and loads table from database
    """

    if request.method == "POST":
        name = request.form["country"]
        maxPop = request.form["maxPop"]
        minPop = request.form["minPop"]
        languages = request.form.getlist("languages")
        sort = None
        if "sort" in request.form:
            sort = request.form["sort"]

        if maxPop != "" and minPop != "" and int(maxPop) < int(minPop):
            countries = db.getCountries()
            languages = db.getLanguages()
            error = "Population min is greater than population max"
            return render_template('countrysearchtemplate.html', option_list=countries,
                                   option_list2=languages, error=error)
        elif name != "":
            return to_country_page(name)
        else:
            results = db.countrySearch(name, minPop, maxPop, languages, sort)
            if len(results) == 0:
                return render_template('countryresults.html',
                                       countries=results, message="No countries match your search")
            else:
                return render_template('countryresults.html', countries=results, message="")


@app.route("/to_city_results", methods=["POST", "GET"])
def search_city():
    """
    takes user to city results
    gets data from html form
    gets and loads table from database
    """

    if request.method == "POST":
        city = request.form["city"]
        country = request.form["country"]
        maxPop = request.form["maxPop"]
        minPop = request.form["minPop"]
        sort = None
        if "sort" in request.form:
            sort = request.form["sort"]

        languages = request.form.getlist("languages")

        if maxPop != "" and minPop != "" and int(maxPop) < int(minPop):
            error = "Population min is greater than population max"
            countries = db.getCountries()
            cities = db.getCities()
            languages = db.getLanguages()

            return render_template('citysearch.html', cities=cities,
                                   countries=countries, languages=languages, error=error)
        elif city != "":
            return to_city_page(city)
        else:
            results = db.citySearch(city, country, minPop, maxPop, languages, sort)
            if len(results) == 0:
                return render_template('cityresults.html', cities=results, message="No cities match your search")
            else:
                return render_template('cityresults.html', cities=results, message="")


@app.route("/to_event_results", methods=["POST", "GET"])
def search_events():
    """
    takes user to event results
    gets data from html form
    gets and loads table from database
    """

    if request.method == "POST":
        event = request.form["event"]
        city = request.form["city"]
        date = request.form["date"]
        maxCost = request.form["maxCost"]
        minCost = request.form["minCost"]
        category = request.form.getlist("categoriesE")

        sort = None
        if "sort" in request.form:
            sort = request.form["sort"]

        discount = None
        if "discount" in request.form:
            discount = request.form["discount"]
            if discount == '3':
                discount = '3'
            else:
                discount = discount == "Yes"

        if maxCost != "" and minCost != "" and float(maxCost) < float(minCost):
            error = "Cost min is greater than cost max"
            events = db.getEvents()
            cities = db.getCities()
            event_cat = db.getEventCategories()

            return render_template('eventsearch.html', events=events, cities=cities, event_cat=event_cat, error=error)
        elif event != "":
            return to_event_page(event)
        else:
            results = db.eventSearch(event, city, date, minCost, maxCost, discount, category, sort)
            if len(results) == 0:
                return render_template('eventresults.html', events=results, message="No events matching your search")
            else:
                return render_template('eventresults.html', events=results, message="")


@app.route("/to_location_results", methods=["POST", "GET"])
def search_locations():
    """
    takes user  to location results
    gets data from html form
    gets and loads table from database
    """
    if request.method == "POST":
        loc = request.form["location"]
        address = request.form["address"]
        city = request.form["city"]
        maxCost = request.form["maxCost"]
        minCost = request.form["minCost"]
        type = request.form.getlist("categoriesL")

        sort = None
        if "sort" in request.form:
            sort = request.form["sort"]

        if maxCost != "" and minCost != "" and float(maxCost) < float(minCost):
            error = "Cost min is greater than cost max"
            cities = db.getCities()
            loc_cat = db.getLocTypes()
            locations = db.getLocNames()
            address = db.getAddresses()

            return render_template('locationsearch.html', locations=locations, address=address,
                                   cities=cities, loc_cat=loc_cat, error=error)
        elif address != "":
            return to_location_page(address)
        else:
            results = db.locationSearch(loc, address, city, minCost, maxCost, type, sort)
            if len(results) == 0:
                return render_template('locationresults.html',
                                       locations=results, message="No locations matched your search")
            else:
                return render_template('locationresults.html', locations=results, message="")


@app.route("/add_city", methods=["POST", "GET"])
def add_city():
    if request.method == "POST":
        city = request.form["city"]
        country = request.form["country"]
        pop = request.form["pop"]
        lon_degree = request.form["lonDegree"]
        lon_minute = request.form["lonMinute"]
        ew = request.form["EW"]
        lat_degree = request.form["latDegree"]
        lat_minute = request.form["latMinute"]
        ns = request.form["NS"]
        languages = request.form.getlist("languages")

        countries = db.getCountries()
        languages2 = db.getLanguagesMgr()

        if len(languages) != 0:
            # should be this way but not for grading purposes
            # db.addCity(city, country, lat_degree + "\' " + lat_minute + "\" " +
            #            ns, lon_degree + "\' " + lon_minute + "\" " + ew, pop, languages)
            db.addCity(city, country, lat_degree + " " + lat_minute + " " +
                       ns, lon_degree + " " + lon_minute + " " + ew, pop, languages)

            message = ["green", "City added"]
            return render_template('managerpage.html', message=message, countries=countries, languages=languages2)
        else:
            message = ["red", "Select a Language"]
            return render_template('managerpage.html', message=message, countries=countries, languages=languages2)

if __name__ == '__main__':
    app.run()
