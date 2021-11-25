import hashlib
import os
from flask import Flask, render_template, request, session
import json
import boto3
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

region_name = "us-east-1"
aws_access_key_id="ASIAZTLANT5OJRZ5BCNE"
aws_secret_access_key="iaoneJNEFCKX7LeJLoiPh2hYPDGnbw6NteyN3G1c"
aws_session_token="FwoGZXIvYXdzELn//////////wEaDDesCj+HHhSRXii+NyK/AS3ex3pPh6LzLoIqvDv0Eob9UeQ77u6uBQ2k2XW1uxHUm7uCsP5r+E6T6+fGR9bSUL7KGOvk2O1jtL3D0eNhBnyxe+YqS9Biq9TcUPbUAxpC+8UYl5ypSpdzplZYf/bWtvTGAH5HtkT9pu4AvySjYDuk+R7NM5QdAExhSVsD1kdAqz8YXVjeQu322WrcBsIEQ+GuWZRzH8e57e3swjpYTcCGHHT2Y2L3qCEuo/K53IAMDRxl2VxmXcmbv5AblV0qKLrAp4MGMi2CjhHS3C46IYieCy+gbQpAtEo84qePaV7+yI/ENnALJNyuc3QTuwW8Zs8mzAE="


s3 = boto3.resource('s3', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

session_aws = boto3.session.Session()
client = session_aws.client(
    service_name='secretsmanager',
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

get_secret_value_response = client.get_secret_value(
    SecretId="snl/hushing/key"
)

salt = json.loads(get_secret_value_response.get('SecretString')).get('hush_key')

clientSns = boto3.client(
    "sns",
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

topic = clientSns.create_topic(Name="notifications")
topic_arn = topic['TopicArn']


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db_password = password + salt
        encrypted_password = str(hashlib.md5(db_password.encode()).hexdigest())
        response = s3.Bucket('group9csci5409').download_file('database.json', 'download.json')
        if response is None:
            with open("download.json") as file:
                data = json.load(file)
                if username == data['username'] and encrypted_password == data['password']:
                    session['username'] = username
                    return render_template('index.html', message="Login Successful")
                elif encrypted_password != data['password']:
                    return render_template('login.html', error="Invalid password")
                else:
                    return render_template('login.html', error="Invalid username")
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        # url = "https://email-checker.p.rapidapi.com/verify/v1"
        # querystring = {"email": str(username)}
        # headers = {
        #     'x-rapidapi-key': "17ac3d6788msha1e8cda5149d5fbp137525jsnaeea3fbea623",
        #     'x-rapidapi-host': "email-checker.p.rapidapi.com"
        #     }
        # response = requests.request("GET", url, headers=headers, params=querystring)
        # print(response.text)
        response = requests.post("https://2dspvabd09.execute-api.us-east-1.amazonaws.com/dev", json={"username": str(username)})
        print(response.content)
        if password == confirm_password:
            db_password = password + salt
            encrypted_password = hashlib.md5(db_password.encode())
            userdata = {
                "username": username,
                "password": str(encrypted_password.hexdigest())
            }

            clientSns.subscribe(
                TopicArn=topic_arn,
                Protocol='email',
                Endpoint=username
            )
            response = clientSns.publish(Message="You are now registered with our application! You will now receive all your updates to"+username, TopicArn=topic_arn)
            print(response)

            # Serializing json
            json_object = json.dumps(userdata, indent=4)
            # Writing to sample.json
            with open("database.json", "w") as outfile:
                outfile.write(json_object)
            response = s3.Bucket('group9csci5409').upload_file('D:\\CSCI5409\\csci-5409-group9-project\\SnakesAndLadders\\database.json', 'database.json')
            print(response)
            return render_template('login.html', message="Signup Successful, Now login with your credentials")
        else:
            return render_template('signup.html', error="User already exists")
    return render_template('signup.html')