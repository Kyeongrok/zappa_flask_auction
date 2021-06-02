from flask import Flask, make_response
from flask import render_template, flash, redirect, url_for, request
from auction_price.domain.dynamo_table import Table
from auction_price.agg.aggregator import agg
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
    return redirect(url_for('statistics'))

@app.route('/api')
def api():
    return {'hello':'world'}

@app.route('/api/statistics', methods=['GET', 'POST'])
def auction_list_api():

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
        retry_cnt -= 1
        date = datetime.datetime.now() + datetime.timedelta(days=retry_cnt)
        date = date.strftime("%Y%m%d")
        r = t.select_statistic(date)

    lek = None
    if r.get( 'LastEvaluatedKey' ) != None:
        lek = r['LastEvaluatedKey']['prdcd_whsal_mrkt_new_cd']

    lst = []
    for i in r['Items']:
        d = ast.literal_eval((json.dumps(i, cls=DecimalEncoder)))
        d['total_cnt'] = int(d['total_cnt'])
        d['prd_cd'] = d['prdcd_whsal_mrkt_new_cd'].split('#')[1]
        if i['agg'].get('상자') != None:
            d['mean_price'] = round(i['agg']['상자']['sum_1prut'] / i['agg']['상자']['cnt'], 0)
        elif i['agg'].get('기타') != None:
            d['mean_price'] = round(i['agg']['기타']['sum_1prut'] / i['agg']['기타']['cnt'], 0)
        else:
            d['mean_price'] = 0
        lst.append(d)
    sorted_lst = sorted(lst, key=lambda k: k['total_cnt'], reverse=True)

    total = len(lst)
    return make_response(json.dumps(sorted_lst, cls=DecimalEncoder))


@app.route('/aggr', methods=['GET', 'POST'])
def aggr():
    date = datetime.datetime.now().strftime("%Y%m%d")
    if request.args.get('date') != None and request.args.get('date') != '':
        date = request.args.get('date')
    prd_cd = request.args.get('prd_cd')
    agg_result = t.select_pk_begins_with(date, f'CRAWL#{prd_cd}')
    # print(last_evaluated_key, l[0])
    prd_nm = agg_result.get('Items')[0]['prd_nm']
    agg_result = agg_result.get('Items')[0]['agg']

    return render_template('agg.html', total=0,
                           agg_result = agg_result,
                           date=date,
                           prd_nm = prd_nm,
                           prd_cd=prd_cd)


@app.route('/auction_list', methods=['GET', 'POST'])
def auction_list():
    '''
    :param prd_cd:
    :return:
    '''
    date = datetime.datetime.now().strftime("%Y%m%d")

    if request.method == 'POST':
        date = request.form['date']
        lek = request.form['last_evaluated_key']
        r = t.select_pk_begins_with(date, lek)
    else:
        if request.args.get('date') != None and request.args.get('date') != '':
            date = request.args.get('date')
        lek = request.args.get('lek')
        prd_cd = request.args.get('prd_cd')
        if lek != None:
            r = t.select_pk_begins_with(date, f'RAW#{prd_cd}', lek=lek)
        else:
            r = t.select_pk_begins_with(date, f'RAW#{prd_cd}')

    # if r['Count'] == 0:
    #     return render_template('auction_list.html', total=0, date=date, prd_cd=prd_cd, title='Auction List')

    last_evaluated_key = r.get('LastEvaluatedKey')
    if last_evaluated_key != None:
        lek = last_evaluated_key['prdcd_whsal_mrkt_new_cd']

    l = []
    for i in r['Items']:
        d = ast.literal_eval((json.dumps(i, cls=DecimalEncoder)))
        l.append(d['data1'])
    total = len(l)
    agg_result = t.select_pk_begins_with(date, f'CRAWL#{prd_cd}', lek=lek)
    # print(last_evaluated_key, l[0])

    return render_template('auction_list.html', total=total, title='Auction List',
                           date = date, prd_cd=prd_cd, prd_nm= '',
                           lek=lek,  list=l)

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
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
        retry_cnt -= 1
        date = datetime.datetime.now() + datetime.timedelta(days=retry_cnt)
        date = date.strftime("%Y%m%d")
        r = t.select_statistic(date)

    if r['Count'] == 0:
        return render_template('statistics.html', result = [], total=0, date=date)

    lek = None
    if r.get( 'LastEvaluatedKey' ) != None:
        lek = r['LastEvaluatedKey']['prdcd_whsal_mrkt_new_cd']

    lst = []
    for i in r['Items']:
        d = ast.literal_eval((json.dumps(i, cls=DecimalEncoder)))
        d['total_cnt'] = int(d['total_cnt'])
        d['prd_cd'] = d['prdcd_whsal_mrkt_new_cd'].split('#')[1]
        if i['agg'].get('상자') != None:
            d['mean_price'] = round(i['agg']['상자']['sum_1prut'] / i['agg']['상자']['cnt'], 0)
        elif i['agg'].get('기타') != None:
            d['mean_price'] = round(i['agg']['기타']['sum_1prut'] / i['agg']['기타']['cnt'], 0)
        else:
            d['mean_price'] = 0
        lst.append(d)
    sorted_lst = sorted(lst, key=lambda k: k['total_cnt'], reverse=True)
    total = len(lst)
    return render_template('statistics.html', result = sorted_lst,
                           total=total, date=date, last_evaluated_key=lek)

@app.route('/std_prdcd_search', methods=['GET', 'POST'])
def std_prdcd_search():
    l = []
    return render_template('std_prdcd_search.html', result = l )
