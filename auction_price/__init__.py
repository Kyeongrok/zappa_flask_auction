from flask import Flask
from flask import render_template, flash, redirect, url_for, request
from auction_price.domain.dynamo_table import Table
from libs.DecimalEncoder import DecimalEncoder
import ast, json
import boto3, datetime

app = Flask(__name__)
t = Table('auction2')

dynamodb = boto3.resource('dynamodb')
def parse_into_json(r):
    l = []
    for i in r['Items']:
        d = ast.literal_eval((json.dumps(i, cls=DecimalEncoder)))
        l.append(d)
    return l

@app.route('/')
def home():
    return redirect(url_for('auction_list'))

@app.route('/api')
def api():
    return {'hello':'world'}

@app.route('/statistic', methods=['GET', 'POST'])
def statistic():
    date = datetime.datetime.now().strftime("%Y%m%d")
    if request.method == 'POST':
        date = request.form['date']
        lek = request.form['last_evaluated_key']

    r = t.select_statistic(date, lek)
    l = parse_into_json(r)

    return render_template('statistic.html', date=date, lek=r['LastEvaluatedKey']['prdcd_whsal_mrkt_new_cd'],
                           items=r['Items'], l = l)

@app.route('/auction_list', methods=['GET', 'POST'])
def auction_list():
    date = datetime.datetime.now().strftime("%Y%m%d")

    if request.method == 'POST':
        date = request.form['date']
        lek = request.form['last_evaluated_key']
        r = t.select_by_pk(date, lek)
    else:
        if request.args.get('date') != None and request.args.get('date') != '':
            date = request.args.get('date')
        r = t.select_by_pk(date)

    if r['Count'] == 0:
        return render_template('auction_list.html', total=0, date=date, title='Auction List')

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
    date = datetime.datetime.now().strftime("%Y%m%d")
    # 모든 작물의 crawl결과를 보여준다 paging으로
    if request.method == 'POST':
        date = request.form['date']
        lek = request.form['last_evaluated_key']

        pass
    # date : default는 오늘이지만 주말, 공휴일이면 가장 빠른 날
    r = t.select_statistic(date)

    retry_cnt = 0
    while retry_cnt < 5 and r['Count'] == 0:
        retry_cnt += 1
        date = datetime.datetime.now() + datetime.timedelta(days=retry_cnt).strftime("%Y%m%d")
        r = t.select_statistic(date)

    if r['Count'] == 0:
        return render_template('crawl_result.html', result = [], total=0, date=date )

    last_evaluated_key = r['LastEvaluatedKey']
    l = []
    for i in r['Items']:
        d = ast.literal_eval((json.dumps(i, cls=DecimalEncoder)))
        l.append(d)
    total = len(l)
    return render_template('crawl_result.html', result = l, total=total, date=date, last_evaluated_key=last_evaluated_key['prdcd_whsal_mrkt_new_cd'] )

@app.route('/std_prdcd_search', methods=['GET', 'POST'])
def std_prdcd_search():
    l = []
    return render_template('std_prdcd_search.html', result = l )
