from flask import Flask, render_template, request, redirect, url_for, make_response, send_file
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import time
from fpdf import FPDF


load_dotenv('config.env')

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
SECRETKEY = os.getenv('SECRETKEY')
LOGOPATH = os.getenv('LOGOPATH')
BUILDINGS = os.getenv('BUILDINGS').strip('[]').split(',')
MONGOURL = os.getenv('MONGOURL')

app = Flask('__name__')

client = MongoClient(MONGOURL)
buildings = client.Attendence.Buildings


def populate_buildings():
    #print(buildings.count())
    if buildings.count() < len(BUILDINGS):
        for building in BUILDINGS:
            if buildings.find_one({'name':building}):
                pass
            else:
                buildings.insert_one({'name':building})

@app.route("/")
def homepage():
    admin_state = 'Sign In'
    if request.cookies.get('SECRETKEY') == SECRETKEY:
        admin_state = "Sign Out"
    else:
        admin_state = 'Sign In'

    list_of_buildings = list()
    for i in buildings.find({},{'name':1}):
        list_of_buildings.append(i['name'])
    context = {
        'all_buildings': list_of_buildings,
        'lost_user':True,
        'current_Date':time.strftime('%a %b %d, %Y',time.localtime()),
        'current_Time':time.strftime('%I:%M %p',time.localtime()),
        'path_to_logo':LOGOPATH,
        'admin_state':admin_state
    }
    return render_template('base.html',**context)



@app.route('/<building>')
def logspage(building):
    admin_state = 'Sign In'
    if request.cookies.get('SECRETKEY') == SECRETKEY:
        admin_state = "Sign Out"
    else:
        admin_state = 'Sign In'

    context={
        'current_Date':time.strftime('%a %b %d, %Y',time.localtime()),
        'current_Time':time.strftime('%I:%M %p',time.localtime()),
        'building':building,
        'lost_user':False,
        'path_to_logo':LOGOPATH,
        'admin_state':admin_state
    }
    return render_template("base.html",**context)



@app.route('/ADDLOG')
def add_values():
    building = request.args.get('building')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    INOROUT = request.args.get('INOROUT')
    date = request.args.get('date')
    time = request.args.get('time')    
    message = ''
    if buildings.find_one({'name': building}) and len(first_name)+len(last_name) > 1:
        if INOROUT == "IN":    
            working_building = buildings.find_one({'name': building},{'_id':0,date:1})
            #return working_building
            if date in working_building:
                working_building[date][first_name+' '+last_name] = {'IN':time,"OUT":'None'}
                buildings.update_one({'name': building},{ '$set':{date: working_building[date]}})
                message = "Success! You've Signed In!"
                return render_template('message.html',message=message)
            else:
                working_building[date] = {first_name+' '+last_name:{'IN':time,"OUT":'None'}}
                buildings.update_one({'name': building},{ '$set':{date: {first_name+' '+last_name:{'IN':time,"OUT":'None'}}}})
                message = "Success! You've Signed In!"
                return render_template('message.html',message=message)
        if INOROUT == "OUT":
            working_building = buildings.find_one({'name': building},{'_id':0,date:1})
            if first_name+' '+last_name not in working_building[date]:
                message = 'Error: The name you entered has not signed in.'
                return render_template('message.html',message=message)
            if date in working_building:
                working_building[date][first_name+' '+last_name]['OUT'] = time
                buildings.update_one({'name': building},{ '$set':{date: working_building[date]}})
                message = "Success! You've Signed Out!"
                return render_template('message.html',message=message)
            else:
                working_building[date] = {first_name+' '+last_name:{'IN':"None","OUT":time}}
                buildings.update_one({'name': building},{ '$set':{date: {first_name+' '+last_name:{'IN':time,"OUT":'None'}}}})
                message = "Success! You've Signed Out!"
                return render_template('message.html',message=message)
    else:
        message = "Error: The building you selected is not in the system please navigate to the home page using the link below."
        return render_template('message.html',message=message)


@app.route("/Logs",methods=['POST'])
def open_logs():
    admin_state = 'Sign In'
    if request.cookies.get('SECRETKEY') == SECRETKEY:
        admin_state = "Sign Out"
    else:
        admin_state = 'Sign In'

    
    if request.form.get("form_action") == 'download':
        return redirect('/Logs/Downloads',307)
    
    if request.cookies.get("SECRETKEY") != SECRETKEY:
        return redirect(url_for('homepage'))   
    list_of_buildings = list()
    for i in buildings.find({},{'name':1}):
        list_of_buildings.append(i['name'])
    list_of_buildings = list()
    for i in buildings.find({},{'name':1}):
        list_of_buildings.append(i['name'])
    
    logs = list()
    building = request.form.get('building')
    dates = []
    date = request.form.get('date')
    
    for i in buildings.find({'name':building},{'_id':0,'name':0}):
        dates+=list(i.keys())
        
    if date:   
        day_logs = buildings.find_one({'name':building},{date:1,"_id":0})
        print(day_logs)
        if len(day_logs.keys()) > 0:
            for i in list(day_logs[date].keys()):
                logs.append(f'{i}  {day_logs[date][i]["IN"]}     {day_logs[date][i]["OUT"]}')
    if building:
        list_of_buildings.remove(building)    
    context = {
        'selected_building':building,
        'selected_date':date,
        'buildings':list_of_buildings,
        'dates':dates,
        'logs':logs,
        'path_to_logo':LOGOPATH,
        'admin_state':admin_state
    }
    return render_template('logs.html', **context)

@app.route("/login",methods=["POST"])
def login():
    username = request.form.get('Username')
    password = request.form.get('Password')
    method_used = request.form.get('admin_state')
    print(request.form)
    if method_used == 'Sign Out':
        response = make_response(redirect(url_for('homepage')))
        response.set_cookie('SECRETKEY',SECRETKEY, max_age=0)
        return response

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        response = make_response(redirect(url_for('open_logs',_method="POST"),307))
        response.set_cookie('SECRETKEY',SECRETKEY)
        return response
    else:
        return render_template("message.html",message="Your Username or Password were incorrect.") 


@app.route("/Logs/Downloads", methods=["POST"])
def download_logs():
    date = request.form.get('date')
    building = request.form.get('building')
    if request.cookies.get("SECRETKEY") == SECRETKEY:
        path = ''
        logs = list()
        pdf = FPDF()
        if date:
            data = buildings.find_one({'name':building},{date:1,"_id":0})
            print(data)
            if len(data.keys()) > 0:
                for i in list(data[date].keys()):
                    logs.append(f'{i}  {data[date][i]["IN"]}     {data[date][i]["OUT"]}')
        
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0,5,building,0,2,"C")
            pdf.cell(0,5,date,0,2,"C")
            pdf.cell(0,5,'NAME                 IN       OUT',0,2,"C")
            for log in logs:
                pdf.cell(0,5,log,0,2,"C")
        response = make_response(pdf.output(dest='S'))
        response.headers.set('Content-Disposition', 'attachment', filename='name' + '.pdf')
        response.headers.set('Content-Type', 'application/pdf')  
        return response
    return render_template('message.html',message='You Dont Have Permission for That.')
if __name__ == "__main__":
    populate_buildings()
    app.run(debug=True)