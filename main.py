from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import time

app = Flask('__main__')

client = MongoClient('mongodb://localhost:27017')
buildings = client.Attendence.Buildings

@app.route("/")
def homepage():
    list_of_buildings = list()
    for i in buildings.find({},{'name':1}):
        list_of_buildings.append(i['name'])
    context = {
        'all_buildings': list_of_buildings,
        'lost_user':True,
        'current_Date':time.strftime('%a %b %d, %Y',time.localtime()),
        'current_Time':time.strftime('%I:%M %p',time.localtime()),
    }
    return render_template('base.html',**context)



@app.route('/<building>')
def logspage(building):
    context={
        'current_Date':time.strftime('%a %b %d, %Y',time.localtime()),
        'current_Time':time.strftime('%I:%M %p',time.localtime()),
        'building':building,
        'lost_user':False
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
            #return working_building
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



if __name__ == "__main__":
    app.run(debug=True)