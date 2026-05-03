import boto3
import uuid
from datetime import datetime
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, DYNAMODB_TABLE

dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

table = dynamodb.Table(DYNAMODB_TABLE)

def create_order(student_name, items, note=""):
    order_id = str(uuid.uuid4())
    order = {
        "order_id": order_id,
        "student_name": student_name,
        "items": items,
        "note": note,
        "status": "bekliyor",
        "created_at": datetime.now().isoformat()
    }
    table.put_item(Item=order)
    return order

def get_all_orders():
    response = table.scan()
    return sorted(response['Items'], key=lambda x: x['created_at'], reverse=True)

def update_order_status(order_id, status):
    table.update_item(
        Key={"order_id": order_id},
        UpdateExpression="SET #s = :s",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": status}
    )
