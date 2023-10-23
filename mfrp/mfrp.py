from flask import Flask, render_template_string, request
import pandas as pd 
import csv
#import os

app=Flask(__name__)

@app.route('/', methods=["GET","POST"])
def index():
    return render_template_string('''<form class="" action="data" method="post"><input type="file" name="csvfile" value=""><input type="submit" name="" value="Submit"></form>''')

@app.route('/data', methods=["GET","POST"])
def data():
    if request.method == 'POST':
        f = request.form['csvfile']
        data=[]
        with open(f) as file:
            csvfile = csv.reader(file)
            for row in csvfile:
                data.append(row)
        data = pd.DataFrame(data)
        # if data.shape[0]<1000:

        return render_template_string('''{{ data | safe }}''', data=data.to_html(header=False))
        # else:
        #     def lambda()

if __name__=='__main__':
    app.run()
    