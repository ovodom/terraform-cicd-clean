import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('NotesTable')

def lambda_handler(event, context):
    print("EVENT:", json.dumps(event))  # debug

    # Handle ALL formats
    method = (
        event.get("requestContext", {}).get("http", {}).get("method")
        or event.get("httpMethod")
    )

    # POST
    if method == "POST":
        body = json.loads(event.get("body") or "{}")

        note_id = str(uuid.uuid4())

        table.put_item(Item={
            "id": note_id,
            "title": body.get("title"),
            "content": body.get("content")
        })

        return {
            "statusCode": 200,
            "body": json.dumps({"id": note_id})
        }

    # GET
    if method == "GET":
        response = table.scan()

        return {
            "statusCode": 200,
            "body": json.dumps(response.get("Items", []))
        }

    return {
        "statusCode": 400,
        "body": json.dumps({
            "error": "Invalid method",
            "received": method
        })
    }