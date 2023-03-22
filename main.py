from flask import *

app = Flask(__name__)

timeslot_dict = {
    "1":"2pm to 3pm",
    "2":"3pm to 4pm",
    "3":"4pm to 5pm",
    "4":"5pm to 6pm"
}

@app.route("/", methods=["get","post"])
def index():
    error = ""
    venue_option = request.form.get("choice")
    #print("venue", venue_option)

    with open("venue.txt", "r") as venues_file: #open venue file for reading only
        venue_data = [] #list of list containing the vacancy of each venue
        for line in venues_file:
            data = line.strip().split(",")
            venue_name, venue_bookings, venue_vacancy = data
            venue_bookings, venue_vacancy = int(venue_bookings), int(venue_vacancy)
            venue_data.append([venue_name, venue_bookings, venue_vacancy])

    if venue_option: #if there is a venue selected
        venue_data_update_text = ""
        venue_data_update = []
        for venue_name, venue_bookings, venue_vacancy in venue_data:
            #print("venue check", venue_name, venue_option)
            if venue_name == venue_option:
                #print("pass")
                if venue_bookings < venue_vacancy:
                    with open("bookings.txt","a") as booking:
                        user_name = request.form.get("name")
                        user_email = request.form.get("email")
                        timeslot = timeslot_dict[request.form.get("timeslot")]
                        booking.write("{},{},{},{}\n".format(user_name, user_email, venue_name, timeslot))
                    venue_bookings += 1
                else:
                    error = "your booking venue {} is not vacant as there is {} people.".format(venue_name, venue_bookings)
            venue_data_update_text += "{},{},{}\n".format(venue_name, venue_bookings, venue_vacancy) #for updating text file
            venue_data_update.append([venue_name, venue_bookings, venue_vacancy]) #for parsing onto the webpage to be displayed
        with open("venue.txt", "w") as venues_file:
            #print("uploaded text", venue_data_update_text)
            venues_file.write(venue_data_update_text) #updating text file
        return render_template("index.html", lst=venue_data_update, error=error)
    else: #if there is no venue selected
        return render_template("index.html", lst=venue_data, error=error)

@app.route("/booking", methods=["get","post"])

def booking():
    with open("venue.txt", "r") as venues_file:  # open venue file for reading only
        venue_data = []  # list of list containing the vacancy of each venue
        for line in venues_file:
            data = line.strip().split(",")
            venue_name, venue_bookings, venue_vacancy = data
            venue_bookings, venue_vacancy = int(venue_bookings), int(venue_vacancy)
            venue_data.append([venue_name, venue_bookings, venue_vacancy])
    name_lst = []
    selected_booking = []
    booking = request.form.get("booking")
    for venue_name, venue_bookings, venue_vacancy in venue_data: #retreiving names of venue for display in table
        name_lst.append(venue_name)
    #print("booking", booking)
    if booking: #if there is a selection
        #print("pass")
        with open("bookings.txt", "r") as booking_file:
            for line in booking_file:
                booking_entry = line.strip().split(",")
                print(booking_entry)
                if booking_entry: #safenet for empty entries
                    booking_user, user_email, booking_venue, booking_timeslot = booking_entry
                    if booking_venue == booking:
                        selected_booking.append(booking_entry)
        return render_template("booking.html", selected_booking=selected_booking, name_lst=name_lst)

    return render_template("booking.html", selected_booking=selected_booking, name_lst=name_lst)

app.run(host='0.0.0.0', port=81)
