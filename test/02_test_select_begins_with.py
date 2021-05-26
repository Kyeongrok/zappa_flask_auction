from auction_price.domain.dynamo_table import Table

if __name__ == '__main__':
    t = Table('auction2')
    r = t.select_pk_begins_with('20210525', 'RAW#1201', lek='RAW#1201#1088')
    for k, v in r.items():
        if k != 'Items':
            print(k)



# stdPrdlstCode 품목코드, date, whsalMrktNewCode
# 왜냐하면 위 두가지 데이터를 기준으로 저장됨
