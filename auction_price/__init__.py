from flask import Flask
from flask import render_template, flash, redirect, url_for, request
from auction_price.domain.dynamo_table import Table
from libs.DecimalEncoder import DecimalEncoder
import ast, json
import boto3

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb')
@app.route('/')
def home():
    return redirect(url_for('auction_list'))

@app.route('/api')
def api():
    return {'hello':'world'}

@app.route('/auction_list', methods=['GET', 'POST'])
def auction_list():
    t = Table('auction2')
    r = t.select_by_pk('20210514')
    l = []
    for i in r['Items']:
        d = ast.literal_eval((json.dumps(i, cls=DecimalEncoder)))
        l.append(d['data1'])
    total = len(l)
    print(l[0])
    return render_template('auction_list.html', total=total, title='Auction List', list=l)
