from flask import *

import boto3 
import csv 
import pandas as pd 
import json

app = Flask(__name__)
from werkzeug.utils import secure_filename

# import key_config as keys

s3 = boto3.client('s3',
                  aws_access_key_id='AKIAVBROUFH5RFFCXM3C',
                  aws_secret_access_key='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',
                  region_name='us-east-2'
                  )

lambda_client = boto3.client('lambda', 
                             aws_access_key_id='AKIAVBROUFH54FYOL4ZE', 
                             aws_secret_access_key='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', 
                             region_name='us-east-2'
                             ) 
# s3 = boto3.client('s3') 
BUCKET_NAME = 'naveen1-bucket'
LAMBDA_NAME = 'demo-lambda'

@app.route('/')
def home():
    return render_template_string('''<!DOCTYPE html>
    <html lang="en">

    <head>
      <meta charset="utf-8" />
      <link rel="apple-touch-icon" sizes="76x76" href="static/img/apple-icon.png">
      <link rel="icon" type="image/png" href="../assets/img/favicon.png">
      <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
      <title>
        HackerShrine
      </title>
      <meta content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0, shrink-to-fit=no' name='viewport' />
      <!-- Fonts and icons -->
      <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700,200" rel="stylesheet" />
      <link href="https://maxcdn.bootstrapcdn.com/font-awesome/latest/css/font-awesome.min.css" rel="stylesheet">
      <!-- CSS Files -->
      <link href="static/css/bootstrap.min.css" rel="stylesheet" />
      <link href="static/css/paper-dashboard.css?v=2.0.1" rel="stylesheet" />
      <!-- CSS -->
      <link href="static/demo/demo.css" rel="stylesheet" />

      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"></script>
    </head>

    <body>
      <div class="navbar">
          <h2> </h2>
      </div>
      <hr>


      <div class="container">
      <h2>HackerShrine</h2>

        <div class="card" style="width:400px">

        <div class="card-body ">
          <form action="/upload" method="post" enctype="multipart/form-data">
          <p class="card-text">Choose a file to upload it to AWS S3</p>
            <input type="file" name="csvfile" value="csvfile">
            <hr>
          <input type="submit" name="upload" value="Upload" class="btn btn-success">
          </form>
          {{msg}}
        </div>
      </div>
      <br>

      <div>
      	<img src="static/images/Lambda SNS.png">
      </div>
    </div>


    </body>

    </html>''')

data2=[] 
@app.route('/upload', methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['csvfile']
        if img: 
            filename = secure_filename(img.filename)
            img.save(filename)
            s3.upload_file(
                Bucket=BUCKET_NAME,
                Filename=filename,
                Key=filename   
            ) 
            #msg = "Upload Done ! "
            
            data=[]
            with open(filename) as file:
                csvfile = csv.reader(file)
                for row in csvfile:
                    data.append(row)
                    data2.append(row)
            data = pd.DataFrame(data)
            
            if data.shape[0]<100: #(rows , columns)
                #return render_template("html1.html", msg=msg)
                if request.method == 'POST':
                    return redirect(url_for('adding'))
                
                #elif request.method == 'GET':
                    
                    #return redirect(url_for('added'))
            else:
                json_string = data.to_json()
                #payload = {'data': json_string}



                response = lambda_client.invoke(
                    FunctionName=LAMBDA_NAME,
                    Payload=str(json_string)) 
                response_payload = response['Payload'].read()
                
                print(response_payload.decode('utf-8'))
                return render_template_string('''{{ data | safe }} <html>
                                                  <h1>Lambda is Triggered check logs</h1>
                                                  <h1>USER ADDING DETAIL FORM</h1>
                                                  <body>
                                                  <form action="{{ url_for('added') }}" method="post">
                                                  First_value :<input name="first_value">
                                                  <br/><br/>
                                                  Second_value :<input name="second_value">
                                                  <br/><br/>
                                                  Third_value : <input name="third_value">
                                                  <br/><br/>
                                                  <button type="submit">Submit</button>
                                                  </form>
                                                  </body>
                                                  </html> ''',data=data.to_html(header=False))
            
@app.route('/adding', methods=['GET','POST'])
def adding():
   
    data = pd.DataFrame(data2)
    #if request.method == 'POST': 
    return render_template_string('''{{ data | safe }} 
                                      <html>
                                      <h1>USER ADDING DETAIL FORM</h1>
                                      <body>
                                      <form action="{{ url_for('added') }}" method="post">
                                      First_value :<input name="first_value">
                                      <br/><br/>
                                      Second_value :<input name="second_value">
                                      <br/><br/>
                                      Third_value : <input name="third_value">
                                      <br/><br/>
                                      <button type="submit">Submit</button>
                                      </form>
                                      </body>
                                      </html> ''',data=data.to_html(header=False))
                                      

@app.route("/added", methods=["GET", "POST"])
def added(): 
    data = pd.DataFrame(data2)
    
    if request.method == "POST":
        first_value=request.form["first_value"] 
        second_value=request.form["second_value"]
        third_value=request.form["third_value"] 
        
        row_s=pd.Series([first_value,second_value,third_value],index=data.columns[2:])
        data = data.append(row_s,ignore_index=True)
        
        data.to_csv('updated.csv', encoding='utf-8')
        s3.upload_file(
            Bucket=BUCKET_NAME,
            Filename="updated.csv",
            Key="updated.csv"
        ) 
        
        client = boto3.client('sns',
                              aws_access_key_id='AKIAVBROUFH5RFFCXM3C',
                              aws_secret_access_key='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',
                              region_name='us-east-2')
        arn='arn:aws:sns:us-east-2:346916399611:mfrp-topic'          #TopicArn of admin group
        subject = f"New Row Added"
        message = f"A new file added to s3-bucket"

        client.publish(                                                 #publishes the alert msg to admin when an user registers
            TopicArn=arn,
            Subject=subject,
            Message=message   
            )
        
        #data.iloc[data.shape[0],3]=request.form["fourth-value"]
        #send subscription mail to user
        
        #return redirect(url_for("yesorno",Email=email,Name=name,Age=age,Mobile=mobile,Place=place,Sub=sub)) #redirect to the url mentioned

        return render_template_string('''{{ data | safe }} <html>

        <h2>Final Results</h2> 

        <body>
            <th> Its done enough</th>

        </body>
        </html>''',data=data.to_html(header=False))

if __name__ == "__main__":
    app.run(debug=True)

