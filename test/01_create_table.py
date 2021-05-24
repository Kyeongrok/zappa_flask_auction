# GSI가 포함된 Table만들기

from auction_price.domain.dynamo_table import Table

if __name__ == '__main__':
    t = Table('aaa')

    t.create_table_with_gsi('auction_prdcd_prdnm')

