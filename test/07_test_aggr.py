from auction_price.domain.dynamo_table import Table
from auction_price.agg.aggregator import agg

def mean_price_update(date, prdcd):
    r = t.select_pk_begins_with(date, f'RAW#{prdcd}', limit=10000)
    m = {'total_cnt':0}
    for item in r['Items']:
        m['total_cnt'] += 1
        data1 = item['data1']
        # print(data1.get('stdFrmlcNewNm'))
        if m.get(data1['stdFrmlcNewNm']) == None:
            m[data1['stdFrmlcNewNm']] = {'cnt':0}
        m[data1['stdFrmlcNewNm']]['cnt'] += 1

    print(m)

if __name__ == '__main__':
    t = Table('auction2')

    mean_price_update('20210526', '1008')
