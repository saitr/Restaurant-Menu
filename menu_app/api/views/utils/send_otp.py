from twilio.rest import Client
from decouple import config
import random

def generate_otp():
    return ''.join(random.choices('0123456789', k=6))





def send_otp_to_user(verified_number):

    print("Inside send_otp_to_user", type(verified_number))
    account_sid = config('OTP_TWILIO_ACCOUNT_SID')
    auth_token =  config('OTP_TWILIO_AUTH_TOKEN')
    verify_sid =  config('VERIFY_SID')
    verify_from_phone_num =  config('OTP_TWILIO_FROM_NUMBER')
    print("account_sid",type(account_sid))
    print("auth_token", type(auth_token))
    print("verify_sid", type(verify_sid))

    client = Client(account_sid, auth_token)
    print("client", client)
    # otp = generate_otp()
    # message = client.messages.create(
    #     body=f"Your OTP is: {otp}",
    #     from_=verify_from_phone_num,
    #     to=phone_number
    # )

    # verified_number = config('VERIFIED_NUMBER')
    print("verified_number type 1", type(verified_number))
    print("verified_number type", verified_number)
    verification = client.verify.v2.services(verify_sid) \
      .verifications \
      .create(to=verified_number, channel="sms")
    print("verification", verification.status)

    return ({"status": verification.status,
             })


def verify_otp(verified_number,entered_otp):
    print("Inside verify_otp")
    print("verified_number type first", type(verified_number))
    # verified_number = config('VERIFIED_NUMBER')
    account_sid = config('OTP_TWILIO_ACCOUNT_SID')
    auth_token = config('OTP_TWILIO_AUTH_TOKEN')
    verify_sid = config('VERIFY_SID')
    print("verified_number type second", type(verified_number))
    client = Client(account_sid, auth_token)

    verification_check = client.verify.v2.services(verify_sid) \
      .verification_checks \
      .create(to=verified_number, code=entered_otp)
    print(verification_check.status)
    return verification_check.status


