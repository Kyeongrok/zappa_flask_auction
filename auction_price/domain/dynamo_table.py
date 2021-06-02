import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
from botocore.exceptions import ClientError

class Table():
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = table_name
        self.table = self.dynamodb.Table(self.table_name)
        self.client = boto3.client('dynamodb')

    def list_table(self):
        response = self.client.list_tables()
        return response

    def create_table(self, table_name, key_schema, attribute_definitions):
        table = self.dynamodb.create_table(
            TableName = table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        print(table)

    def create_table_with_gsi(self, table_name):
        response = self.dynamodb.create_table(
            TableName = table_name,
            KeySchema=[
                {
                    'AttributeName': 'prdcd',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'prdnm',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'prdcd',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'prdnm',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        return response

    def insert(self, row):
        r = self.table.put_item(Item=row)
        return r

    def select_all(self):
        r = self.table.scan()
        return r

    def select_by_pk(self, pk, last_evaluated_key=None):
        if last_evaluated_key == None:
            response = self.table.query(
                KeyConditionExpression=Key('date').eq(pk),
                Limit=100
            )
        else:
            response = self.table.query(
                KeyConditionExpression=Key('date').eq(pk),
                ExclusiveStartKey = {'date':pk, 'prdcd_whsal_mrkt_new_cd':last_evaluated_key},
                Limit=100
            )

        return response

        # table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

    def select_by_sk(self, sk, last_evaluated_key=None, limit=100):
        response = self.table.query(
            KeyConditionExpression=Key('date').eq(sk),
            Limit=limit
        )

        return response

    def select_by_sth(self):
        '''
        eq, begins with, between, contains, in,
        '''
        response = self.table.query(
            KeyConditionExpression = Key('date').eq('20210509') & Key('wcode').eq(2)
        )
        print(response)


    def select_pk_begins_with(self, date, begins='1202', lek=None, limit=100):
        if lek == None:
            response = self.table.query(
                KeyConditionExpression = Key('date').eq(date) & Key('prdcd_whsal_mrkt_new_cd').begins_with(f'{begins}'),
                Limit = limit
            )
        else:
            response = self.table.query(
                KeyConditionExpression = Key('date').eq(date) & Key('prdcd_whsal_mrkt_new_cd').begins_with(f'{begins}'),
                ExclusiveStartKey = {'date':date, 'prdcd_whsal_mrkt_new_cd':lek},
                Limit = limit
            )

        return response

    def select_pk_sk(self, pk, sk):
        response = self.table.query(
            KeyConditionExpression = Key('date').eq(pk) & Key('prdcd_whsal_mrkt_new_cd').eq(sk)
        )
        return response

    def select_statistic(self, pk, lek=None, limit=100):
        if lek == None:
            response = self.table.query(
                KeyConditionExpression = Key('date').eq(pk) & Key('prdcd_whsal_mrkt_new_cd').begins_with('CRAWL#'),
                FilterExpression = 'total_cnt > :v',
                ExpressionAttributeValues= {
                    ':v': 0,
                },
                Limit=limit
            )
        else:
            response = self.table.query(
                KeyConditionExpression = Key('date').eq(pk) & Key('prdcd_whsal_mrkt_new_cd').begins_with('CRAWL#'),
                ExclusiveStartKey = {'date':pk, 'prdcd_whsal_mrkt_new_cd':lek},
                FilterExpression = 'total_cnt > :v',
                ExpressionAttributeValues= {
                    ':v': 0,
                },
                Limit=100
            )

        return response

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


    def update_prdnm(self, pk, sk, prdnm):

            response=self.table.update_item(
                Key={
                    'date': pk,
                    'prdcd_whsal_mrkt_new_cd': sk
                },
                UpdateExpression="set prdnm=:n",
                ExpressionAttributeValues={
                    ':n': prdnm,
                },
                ReturnValues="UPDATED_NEW"
            )
            return response

    def delete(self, pk, sk):
        try:
            response = self.table.delete_item(
                Key={
                    'date': pk,
                    'prdcd_whsal_mrkt_new_cd': sk
                }
            )
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise

