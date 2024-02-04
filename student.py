import boto3
import datetime
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Todo-n63vfsdwvfemhcta2v7ysyrrwy-staging')
def validate(slots):
    if not slots['order']:
        print("Inside Empty Location")
        return {
            'isValid': False,
            'violatedSlot': 'order'
        }
    if not slots['rollno']:
        print("Inside Empty Location")
        return {
            'isValid': False,
            'violatedSlot': 'rollno'
        }
    if not slots['deliveryTime']:
        print('Inside empty location')
        return{
            'isValid': False,
            'violatedSlot': 'deliveryTime'
        }
    return { 'isValid':True }
def lambda_handler(event, context):
    # TODO implement
    foodList = ""
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    print(event)
    print(slots)
    validation_result = validate(slots)
    print(validation_result)
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit':validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                        }
                    }
               }
        else:
            roll=slots['rollno']['value']['originalValue']
            order=slots['order']['value']['originalValue']
            delivery=slots['deliveryTime']['value']['originalValue']
            timezone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))  # India timezone example
            current_time = datetime.datetime.now(timezone)
            current_time=current_time.strftime("%H:%M:%S")
            print("Current time:", current_time)
            table.put_item(
                Item = {
                    'id': roll , 
                    'rollno': roll ,
                    'order' : order ,
                    'delivery'  : delivery+"" ,
                    'createdAt' : '2022-11-25T16:11:24.977Z' ,
                    'updatedAt' : '2022-11-25T16:11:24.977Z'
                }
            )
    return response
    
    
