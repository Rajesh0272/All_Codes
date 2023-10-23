import boto3
import re
from data_mod import *
    
    
# Trigger SNS message admin
def trigger_sns_message_admin(email, name):
    # Connect to SNS
    
    client = boto3.client('sns',
                          aws_access_key_id='AKIAVBROUFH5QNUFO72E',
                          aws_secret_access_key='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',
                          region_name='us-east-2')
    arn='arn:aws:sns:us-east-2:346916399611:group-4-admin-topic'          #TopicArn of admin group
    subject = f"New user registered: {name}"
    message = f"A new user has registered with {name}."

    client.publish(                                                 #publishes the alert msg to admin when an user registers
        TopicArn=arn,
        Subject=subject,
        Message=message   
        )
    
# Trigger SNS message user for subscription
def trigger_subscribe(email, name):
    # Connect to SNS
    client = boto3.client('sns',
                          aws_access_key_id='AKIAVBROUFH5QNUFO72E',
                          aws_secret_access_key='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',
                          region_name='us-east-2')
    arn='arn:aws:sns:us-east-2:346916399611:group-4-user-topic'         #TopicArn of user group

    response=client.subscribe(                                      #subscribe action will send a mail to the mail-ID for subscription confirmation
        TopicArn=arn,
        Protocol='email',                                           #client.subscribe will return a dict containing SubscriptionArn
        Endpoint=email,                                             #endpoint is the email-ID user inputs
        ReturnSubscriptionArn=True
        )
    x=response['SubscriptionArn']                                   #gets value of the SubscriptionArn key in the dictionary
    return x
    

def trigger_publish(email, name,sub):
    # Connect to SNS
    client = boto3.client('sns',
                          aws_access_key_id='AKIAVBROUFH5QNUFO72E',
                          aws_secret_access_key='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',
                          region_name='us-east-2')
    arn='arn:aws:sns:us-east-2:346916399611:group-4-user-topic'         #TopicArn of user group
    subject = f"user registered: {name}"
    message = f"You have been successfully registered as an user.\nregards,\nadmin"

    client.publish(                                                 #publishes the alert msg to admin when an user registers
    TopicArn=arn,
    Subject=subject,
    Message=message   
    )
    #print("Registered")

    client.unsubscribe(
        SubscriptionArn=sub
        )
        

