
from flask import *
#from data_mod import *
#from sns_pro import *

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])

def home():

    if request.method == "POST":
        name=request.form["name"]
        age=request.form["age"]
        mobile=request.form["mob"]
        email=request.form["email"]
        place=request.form["place"]
        
        sub=trigger_subscribe(email, name)      #send subscription mail to user
        
        return redirect(url_for("yesorno",Email=email,Name=name,Age=age,Mobile=mobile,Place=place,Sub=sub)) #redirect to the url mentioned

    return render_template("index.html")

@app.route("/yesorno/<Email>&<Name>&<Age>&<Mobile>&<Place>&<Sub>", methods=["GET", "POST"])

def yesorno(Email,Name,Age,Mobile,Place,Sub):
    
    
    if request.method == "POST":
        name=request.form["val"]
        if name.lower()=="yes" :
            
            trigger_publish(Email, Name, Sub)
            store_user_info(Name, Age, Mobile, Email, Place)
            trigger_sns_message_admin(Email, Name)
        else:
            return ("Sorry! you didn't subscribe to the topic")
        
        #l=sel_data()
        return ("Registration Successful")

       
        
    return render_template("index2.html")

if __name__ == "__main__":
    app.run(debug=True)
  
