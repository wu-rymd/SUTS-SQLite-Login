#! /usr/bin/python


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
#  Raymond Wu  /  Th 2018-07-19
#
#  Flask web application as proof-of-concept
#    for simple SQLite database manipulation
#    using user registrations and log-ins
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#  TO-DO:
#
#  ---> How to get string representations of entries in table?
#    fName = database.execute("SELECT firstName from credentials where email = (?)", [uEmail])
#    lName = database.execute("SELECT lastName from credentials where email = (?)", [uEmail])
#
#  ---> User session --> Logout
#    Look into Flask-Session
#
#  ---> How to encrypt/password-protect database file?
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 



# Flask:            run flask app
# render_template:  render webpage
# request:          process data from form

from flask import Flask, render_template, request

# sqlite3:          database

import sqlite3



app = Flask(__name__)



# redirect to home page
@app.route('/')
def default():
    return render_template('/index.html');



# home page
@app.route('/index.html')
def index():
    return render_template('/index.html');



# log in page
@app.route('/login.html')
def login():
    return render_template('/login.html');

    

# register page
@app.route('/register.html')
def register():  
    return render_template('/register.html');




# page solely for authorizing log in/registration
@app.route('/auth.html', methods = ['POST'])
def auth():


    # using only POST method to hide query parameters/values in URL
    
    # KEEP IN THIS METHOD TO AVOID sqlite3.ProgrammingError:
    # SQLite objects created in a thread can only be used in that same thread.
    
    # open the database
    connection = sqlite3.connect("database.db")
    database = connection.cursor()
    
    # create the database -- if doesn't already exist
    try:
        database.execute('CREATE TABLE credentials (id REAL, firstName TEXT, lastName TEXT, school TEXT, email TEXT, password TEXT)')
    except sqlite3.OperationalError:
        pass


    

    # determine which form submitted

    try:    
        action = request.form['submit']
        print action
    except:
        action = "UNDEFINED"

    

    # if from LOGIN
    if action == "Log in":
        
        uEmail = request.form['email']        #  .form[] for POST method  (vs. .args[] for query parameters / GET method)
        uPass = request.form['pass']
        
        gEmail = database.execute("SELECT email from credentials where email = (?)", [uEmail])
        emailExists = gEmail.fetchone()

        if emailExists:
            # does password match that of email?
            gPass = database.execute("SELECT password from credentials where email = (?)", [uEmail])
            actualPass = gPass.fetchone()

            if uPass == actualPass[0]:
                # fName = database.execute("SELECT firstName from credentials where email = (?)", [uEmail])
                # lName = database.execute("SELECT lastName from credentials where email = (?)", [uEmail])

                connection.commit()
                connection.close()
    
                retStr = "<h1> Hi, " + uEmail + "! </h1> <br>"
                return retStr + render_template('/index.html')

            else:
                connection.commit()
                connection.close()
                
                retStr = "<h1> Incorrect password! </h1> <br>"
                return retStr + render_template('/index.html')
        else:
            connection.commit()
            connection.close()
            
            retStr = "<h1> That e-mail doesn't exist! </h1> <br>"
            return retStr + render_template('/index.html')


        
    # if from REGISTER
    elif action == "Register":
        uFirstName = request.form['firstName']     #  .form[] for POST method  (vs. .args[] for query parameters / GET method)
        uLastName = request.form['lastName']
        uSchool = request.form['school']
        uEmail = request.form['email']
        uPass = request.form['pass']


        # checking to see if e-mail already exists in database
        # do not allow duplicate e-mail registrations
        
        gEmail = database.execute("SELECT email from credentials where email = (?)", [uEmail])
        emailExists = gEmail.fetchone()

        if emailExists:
            retStr = "<h2> That e-mail is already taken! </h2> <br>"
            return retStr + render_template('/index.html')


        else:
        
            # add data
            database.execute('INSERT INTO credentials (firstName, lastName, school, email, password) VALUES ("' + uFirstName + '", "' + uLastName + '", "' + uSchool + '", "' + uEmail + '", "' + uPass + '")')
        
            connection.commit()
            connection.close()
    
            retStr = "<h1> Account created! </h1> <br>"
            return retStr + render_template('/index.html')


    # value of name="submit" submit button not in ['Log in', 'Register']
    elif action == "UNDEFINED":
        connection.commit()
        connection.close()
    
        retStr = "<h2> Action undefined... </h2> <br>"
        return retStr + render_template('/auth.html')

        

    # value of name="submit" submit button not in ['Log in', 'Register']
    else:
        connection.commit()
        connection.close()
    
        retStr = "<h2> Unexpected error... </h2> <br>"
        return retStr + render_template('/auth.html')


    connection.commit()
    connection.close()
    

# run the app!
if __name__ == '__main__':
   app.run(debug = True)
