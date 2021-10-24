
from pprint import pprint
from decimal import Decimal
import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
counter_db_tablename = os.environ['DBTableName']

# TODO: Better structure table class
class CounterDB:
    """ DynamoDB Table Class """

    def get_localDB(self):
        """ Set up local DB

        Returns
        ------
        Local DynamoDB instance at PORT: dict

        """
        return boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    def inc_count(self, dynamodb=None):
        """ Increment global counter at DB

        Parameters
        ----------
        dynamodb: dict, optional
        AWS Dynamodb instance form

        Returns
        ------
        Global request count at DB: number

        """
        if not dynamodb:
            # Point to local DB
            dynamodb = self.get_localDB()

        table = dynamodb.Table(counter_db_tablename)
        pprint(f"Increment service request count")

        get_response = table.get_item(
            Key={
                'id': 'GLOBAL_COUNT'
            }
        )

        try:
            current_count = get_response['Item']['count']
        except KeyError:
            print('initalizing global count')
            try:
                table.put_item(
                    Item={
                        'id': 'GLOBAL_COUNT',
                        'count': 1
                    }
                )
                return 1
            except Exception as e:
                print('db initalization failed')
                print(e)
                raise Exception("db initialization failed")


        table.update_item(
            Key={
                'id': 'GLOBAL_COUNT'
            },
            UpdateExpression='SET #COUNT = :COUNT',
            ConditionExpression='#COUNT <> :COUNT',
            ExpressionAttributeNames={'#COUNT': 'count'},
            ExpressionAttributeValues={':COUNT': current_count + 1 }
        )

        return current_count + 1

    def reset_count(self, dynamodb=None):
        """ Reset global counter at DB

        Parameters
        ----------
        dynamodb: dict, optional
        AWS Dynamodb instance form

        Returns
        ------
        Global request count at DB: number

        """

        if not dynamodb: 
            # Point to local DB
            dynamodb = self.get_localDB()

        table = dynamodb.Table(counter_db_tablename)
        pprint(f"Reset service request count")

        table.update_item(
            Key={
                'id': 'GLOBAL_COUNT'
            },
            UpdateExpression='SET #COUNT = :COUNT',
            ExpressionAttributeNames={'#COUNT': 'count'},
            ExpressionAttributeValues={':COUNT': Decimal('0') }
        )

def lambda_handler(event, context):
    """ Load counter and reset Lambda

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

    context: object, required
        Lambda Context runtime methods and attributes

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

    """

    try:
        if event['path'] == '/':
            count = CounterDB().inc_count(dynamodb)
            return {
                "statusCode": 201,
                "headers": {'content-type': 'application/json'},
                "body": json.dumps({ 'message': f"{count}" })
            }
        if event['path'] == '/reset':
            CounterDB().reset_count(dynamodb)
            return {
                "statusCode": 201,
                "headers": {'content-type': 'application/json'},
                "body": '{\"message\": \"0\"}'
            }

    except Exception as e:
        pprint('ops failure !')
        pprint(e)

        return {
            "statusCode": 500,
            "headers": {'content-type': 'application/json'},
            "body": '{\"error\": \"Server failed to process request\"}'
        }

    return {
        "statusCode": 400,
        "headers": {'content-type': 'application/json'},
        "body": '{\"error\": \"invalid request\"}'
    }

if __name__ == '__main__':
    # TODO: Add checks for run 
    pass