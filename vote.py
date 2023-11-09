from flask import Flask, render_template, request, session, redirect, url_for,flash
import os
import csv
import pandas as pd
app = Flask(__name__)



# The app.config dictionary is a general-purpose place to store configuration variables
# used by the framework, the extensions, or the application itself. Configuration values
# can be added to the app.config object using standard dictionary syntax.

# The SECRET_KEY configuration variable is used as a general-purpose encryption key by
# Flask and several third-party extensions. As its name implies, the strength of the en‐
# cryption depends on the value of this variable being secret.
app.config['SECRET_KEY'] = 'hard to guess string'

candidates = [
    {
        "id": 0,
        "name": "Saurav Shrestha",
        "manifesto": "I promise to improve education and healthcare for all citizens.",
        "votes": 0
    },
    {
        "id": 1,
        "name": "Obaloluwa Akinloye",
        "manifesto": "I will focus on creating more job opportunities and boosting the economy.",
        "votes": 0
    },
    {
        "id": 2,
        "name": "Ridwan Adekilekun",
        "manifesto": "I am committed to environmental protection and sustainability.",
        "votes": 0
    },
    {
        "id": 3,
        "name": "Blessing Okoro",
        "manifesto": "I aim to reduce crime rates and improve public safety.",
        "votes": 0
    }
    ,
    {
        "id": 4,
        "name": "Igbanam Iwowari",
        "manifesto": "I will focus on creating more job opportunities and boosting the economy.",
        "votes": 0
    }
    ,
    {
        "id": 5,
        "name": "Idris Umeni",
        "manifesto": "I promise to improve education and healthcare for all citizens.",
        "votes": 0
    },
    {
        "id": 6,
        "name": "Desmond Mbun",
        "manifesto": "I am committed to environmental protection and sustainability.",
        "votes": 0
    }
    
    ]

'''Decorators are a standard feature of the Python language; they can
modify the behavior of a function in different ways. A common pat‐
tern is to use decorators to register functions as handlers for an event 

The app.route registers the decorated function as a route

'''

@app.route('/')
def home():
    return render_template("home.html", candidates = candidates)
@app.route('/test')
def test():
    return render_template("test.html", candidates = candidates)


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        data = {'Name': name, 'Email': email, 'Password': password, 'CanVote' : True }

        if not os.path.exists('data.csv'):
            with open('data.csv', 'w', newline='') as csvfile:
                fieldnames = ['Index', 'Name', 'Email', 'Password', 'CanVote']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                data['Index'] = 0 
                writer.writerow(data)
        else:
            with open('data.csv', 'a', newline='') as csvfile:
                fieldnames = ['Index', 'Name', 'Email', 'Password','CanVote']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                with open('data.csv', 'r') as file:
                    lines = list(csv.DictReader(file))
                    last_index = int(lines[-1]['Index']) + 1
                    data['Index'] = last_index
                writer.writerow(data)
            flash('You were successfully Created New Account..')
        return redirect("/register")
    else:
        return render_template('login.html')



@app.route("/login_check", methods=["POST","GET"])
def login_check():
    if not os.path.exists('data.csv'):
        flash('No Such Id found')
        return redirect('/register')
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Name and password verification using CSV file
        if check_credentials(email, password):
            response = "Login successful!"
            session['logged_in'] = True  # Store the logged-in status in the session
            # --------------------------
            # getting username from csv
            with open("data.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    row_values = list(row)
                    if row_values[2] == email:
                        session['user_name']= row_values[1]
                        session['email'] = email
            # /////////////////////////
            flash('You were successfully logged in')
            return redirect('/')
        else:
            flash('Enter valid detail to login')
            response = "Invalid credentials. Please try again."
            session['logged_in'] = False  # Store the logged-in status in the session
            return redirect('/register')
    else:
        pass
    
@app.route('/vote/<int:id>')    
def vote(id):
    
    if session.get('logged_in') == True:    
        user_detail = file_checker(session['email'], file='data.csv' ,mode='r')   
        if user_detail["CanVote"] == 'True':
            candidate = candidates[id]
            return render_template("vote.html", candidate=candidate)
        else:
            flash('You have already voted !!!')
            return render_template("home.html", candidates = candidates)

    flash('You must login first to vote !!!')
    return redirect("/register")


@app.route('/dashboard')
def dashboard():
     return render_template("dashboard.html",candidates = candidates )    

@app.route('/logout')
def log_out():
    if session.get('logged_in') == True:
       session['logged_in'] = False
       print(session)
       session.pop('user_name', None)
       session['email'] = ''
       print(session)
       flash('You were successfully logged Out')
    return redirect("/")

def check_credentials(email, password):
    with open("data.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            row_values = list(row)
            if row_values[2] == email and row_values[3] == password:
                return True
    return False

@app.route('/vote/cast/<int:id>')
def cast(id):
   
    if session.get('logged_in') == True:
        
        user_detail = file_checker(session['email'], file='data.csv' ,mode='r')
        if user_detail["CanVote"] == 'True':
            df_vote = pd.read_csv('data.csv')     
            voted_index = df_vote[df_vote['Email'] == session['email']].index
            if not voted_index.empty:
                df_vote.at[voted_index[0], 'CanVote'] = False
            df_vote.to_csv("data.csv", index=False)  

            candidate = candidates[id]
            candidate['votes'] += 1             
            return render_template("dashboard.html",candidates = candidates )          
        else:
            flash('You have already voted')
            return redirect('/dashboard')

    return redirect("/register")


def file_checker(find_email, file=None, mode='r'):
    can_vote = False
    try:
        with open('data.csv' , 'r') as csvfile:
            reader = csv.reader(csvfile)
            header_row = next(reader)
            email_indx = header_row.index("Email")
            
            print('-'*20)
            for row in reader:
                if row[email_indx] == find_email:
                    new_dict = dict(zip(header_row, row))
                    return new_dict

    except Exception as e:
        print(e)
        return can_vote
    else:
        return can_vote       
                 
# @app.route('/vote/cast/<int:id>')
# def cast(id):
#     if session.get('logged_in') == True:
#             
            
#         candidate = candidates[id]
#         candidate['votes'] += 1
#         return render_template("dashboard.html",candidates = candidates )

#     return redirect("register")


if __name__ == '__main__':
    app.run(debug=True ,port=80)