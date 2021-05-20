from flask import Flask
from flask import render_template, flash, redirect, url_for, request
from auction_price.domain.dynamo_table import Table
from libs.DecimalEncoder import DecimalEncoder
import ast, json
import boto3

app = Flask(__name__)
t = Table('auction2')

dynamodb = boto3.resource('dynamodb')
@app.route('/')
def home():
    return redirect(url_for('auction_list'))

@app.route('/api')
def api():
    return {'hello':'world'}

@app.route('/statistic')
def statistic():
    return render_template('statistic.html')

@app.route('/auction_list', methods=['GET', 'POST'])
def auction_list():
    date = '20210514'

    if request.method == 'POST':
        date = request.form['date']
        lek = request.form['last_evaluated_key']
        r = t.select_by_pk(date, lek)
    else:
        if request.args.get('date') != None and request.args.get('date') != '':
            date = request.args.get('date')
        r = t.select_by_pk(date)

    last_evaluated_key = r['LastEvaluatedKey']

    l = []
    for i in r['Items']:
        d = ast.literal_eval((json.dumps(i, cls=DecimalEncoder)))
        l.append(d['data1'])
    total = len(l)
    print(last_evaluated_key, l[0])
    return render_template('auction_list.html', total=total, title='Auction List',
                           date = date,
                           last_evaluated_key=last_evaluated_key['prdcd_whsal_mrkt_new_cd'],  list=l)

@app.route('/crawl_result', methods=['GET', 'POST'])
def crawl_result():
    # 모든 작물의 crawl결과를 보여준다 paging으로
    # date : default는 오늘이지만 주말, 공휴일이면 가장 빠른 날
    r = t.select_pk_begins_with('20210517', 'CRAWL')
    l = []
    for i in r['Items']:
        d = ast.literal_eval((json.dumps(i, cls=DecimalEncoder)))
        l.append(d)
    total = len(l)
    return render_template('crawl_result.html', result = l, total=total)
