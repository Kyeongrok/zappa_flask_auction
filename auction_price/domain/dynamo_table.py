import boto3
from boto3.dynamodb.conditions import Key

class Table():
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = table_name
        self.table = self.dynamodb.Table(self.table_name)
        self.client = boto3.client('dynamodb')

    def list_table(self):
        response = self.client.list_tables()
        return response

    def create_table(self, key_schema, attribute_definitions):
        table = self.dynamodb.create_table(
            TableName = self.table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        print(table)

    def insert(self, row):
        r = self.table.put_item(Item=row)
        return r

    def select_all(self):
        r = self.table.scan()
        return r

    def select_by_pk(self, pk, last_evaluated_key=None):
        response = self.table.query(
            KeyConditionExpression=Key('date').eq(pk),
            Limit=100
        )

        return response

        # table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        # print(f'{table_name} has been created')
    def select_by_sth(self):
        '''
        eq, begins with, between, contains, in,
        '''
        response = self.table.query(
            KeyConditionExpression = Key('date').eq('20210509') & Key('wcode').eq(2)
        )
        print(response)


    def select_pk_begins_with(self, date, prd_cd='1202'):
        response = self.table.query(
            KeyConditionExpression = Key('date').eq(date) & Key('prdcd_whsal_mrkt_new_cd').begins_with(f'{prd_cd}#')
        )
        print(response)

    def insert_into_db(self, jo, date, prd_cd, rnum):
        # print(jo)
        row = {
            'date': f'{date}',
            'prdcd_whsal_mrkt_new_cd': f'{prd_cd}#{rnum}',
            'data1': jo
        }
        try:
            self.insert(row)
        except Exception as e:
            print(e)
            print('error:', date, prd_cd, rnum)
            exit(0)
