from auction_price.domain.dynamo_table import Table
import csv, json


def read_csv_file_into_list(filename, delimiter=',', encoding='utf-8'):
    with open(filename, newline='', encoding=encoding) as f:
        ll = csv.reader(f, delimiter=delimiter)
        return list(ll)

def f():
    with open('std_prd_cd.json') as f:
        m = json.loads(f.read())

    r = t.select_pk_begins_with('20210521', 'CRAWL', limit=2000)

    for item in r['Items']:
        print(item['date'], item['prdcd_whsal_mrkt_new_cd'])
        prdcd = item['prdcd_whsal_mrkt_new_cd'].split('#')[1]
        ur = t.update_prdnm(item['date'], item['prdcd_whsal_mrkt_new_cd'], m[prdcd])
        print(ur)

if __name__ == '__main__':
    t = Table('auction2')

    # 오늘날짜를 select
    r = t.select_pk_begins_with('20210524', 'RAW#1001', limit=2000)
    for item in r['Items']:
        print(item)





