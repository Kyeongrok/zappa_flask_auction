
from auction_price.domain.dynamo_table import Table

def agg(date, prdcd):
    t = Table('auction2')
    r = t.select_pk_begins_with(date, f'RAW#{prdcd}', limit=10000)
    # m = {'total_cnt':0}
    m = {}
    for item in r['Items']:
        # m['total_cnt'] += 1
        data1 = item['data1']
        # print(data1.get('stdFrmlcNewNm'))
        if m.get(data1['stdFrmlcNewNm']) == None:
            m[data1['stdFrmlcNewNm']] = {'cnt':0, 'sum_1prut':0}
        m[data1['stdFrmlcNewNm']]['cnt'] += 1

        # row당 1kg로 환산해서 더함
        m[data1['stdFrmlcNewNm']]['sum_1prut'] += round(data1['sbidPric'] / data1['delngPrut'], 2)


    return m