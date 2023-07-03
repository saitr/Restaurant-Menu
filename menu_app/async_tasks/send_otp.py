from twilio.rest import Client
from decouple import config
from celery import shared_task

@shared_task()
def send_otp_to_user(verified_number):
    print("Inside send_otp_to_user")
    account_sid = config('OTP_TWILIO_ACCOUNT_SID')
    auth_token =  config('OTP_TWILIO_AUTH_TOKEN')
    verify_sid =  config('VERIFY_SID')



    client = Client(account_sid, auth_token)

    verification = client.verify.v2.services(verify_sid) \
      .verifications \
      .create(to=verified_number, channel="sms")
    print(verification.status)

    return verification.status

@shared_task()
def verify_otp(post_set,verification_status):
    account_sid = config('OTP_TWILIO_ACCOUNT_SID')
    auth_token = config('OTP_TWILIO_AUTH_TOKEN')
    verify_sid = config('VERIFY_SID')
    verified_number = config('VERIFIED_NUMBER')

    client = Client(account_sid, auth_token)

    otp_code = input("Please enter the OTP:")

    verification_check = client.verify.v2.services(verify_sid) \
      .verification_checks \
      .create(to=verified_number, code=otp_code)
    print(verification_check.status)


