import boto3
from botocore.exceptions import ClientError

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = "sender@gmail.com"

# Replace recipient@example.com with a "To" address. If your account 
# is still in the sandbox, this address must be verified.


# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the 
# ConfigurationSetName=CONFIGURATION_SET argument below.
#CONFIGURATION_SET = "ConfigSet"

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-east-1"

# The subject line for the email.
SUBJECT = "IT Support Ticket"

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("Amazon SES LEX Ticket Tool"
            )
            


def setup_email_body(contextData):
    # The HTML body of the email.
    device = contextData['currentIntent']['slots']['Device']
    email = contextData['currentIntent']['slots']['Email']
    problem = contextData['currentIntent']['slots']['Problem']
    BODY_HTML = """<html>
    <head>Support Ticket</head>
    <body>
    <h1>We have logged a ticket based on your request</h1>
    <p>Ticket Details are</p>
    <p>Device: %s </p>
    <p>Problem: %s </p>
    <p>Raised by: %s </p>
    </body>
    </html> """
    return BODY_HTML  % (device,problem,email)

# The character encoding for the email.
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=AWS_REGION)

def lex_email(event=None,context=None):
    print('event data --->',event)
    print('context data -->',context)
    RECIPIENT = event['currentIntent']['slots']['Email']
    # Try to send the email.
    if event['currentIntent']['slots']['Email'] is not None:

        try:
            #Provide the contents of the email.
            
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': setup_email_body(event),
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
            )
        # Display an error if something goes wrong.	
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
            response = {
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState": "Fulfilled",
                    "message": {
                    "contentType": "SSML",
                    "content": "Email was sent successfully with message id as {messageId} ".format(messageId=response['MessageId'])
                    },
                }
            }
            print('result = ' + str(response))
            return response
    else:
            response = {
                    "dialogAction": {
                        "type": "Close",
                        "fulfillmentState": "Fulfilled",
                        "message": {
                        "contentType": "SSML",
                        "content": "Some error occrured"
                        },
                    }
                }
            print('result = ' + str(response))
            return response