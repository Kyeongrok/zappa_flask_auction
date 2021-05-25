from auction_price.domain.dynamo_table import Table

if __name__ == '__main__':
    t = Table('auction2')
    pk = '20210524'
    for sk in ['1013', '1014']:
        r = t.select_pk_begins_with(pk, sk, limit=2000)

        for itm in r['Items']:
            skk = f'{sk}#{itm["data1"]["rnum"]}'
            print(skk)
            res = t.delete(pk, skk)
            print(res)
