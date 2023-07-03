from twilio.rest import Client
from decouple import config


def send_otp_to_user(phone_number):
    print("Inside send_otp_to_user")
    account_sid = config('OTP_TWILIO_ACCOUNT_SID')
    auth_token =  config('OTP_TWILIO_AUTH_TOKEN')
    verify_sid =  config('VERIFY_SID')
    client = Client(account_sid, auth_token)

    verification = client.verify.v2.services(verify_sid) \
      .verifications \
      .create(to=phone_number, channel="sms")
    print(verification.status)

    return verification.status


def verify_otp(verified_number,entered_otp):
    print("Inside verify_otp")
    account_sid = config('OTP_TWILIO_ACCOUNT_SID')
    auth_token = config('OTP_TWILIO_AUTH_TOKEN')
    verify_sid = config('VERIFY_SID')

    client = Client(account_sid, auth_token)

    verification_check = client.verify.v2.services(verify_sid) \
      .verification_checks \
      .create(to=verified_number, code=entered_otp)
    print(verification_check.status)
    return verification_check.status


