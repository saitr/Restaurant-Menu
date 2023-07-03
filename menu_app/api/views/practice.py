from twilio.rest import Client
from decouple import config

account_sid = config('OTP_TWILIO_ACCOUNT_SID')
# account_sid = 'VA1a115faeddad2907d3b6503da511f712'
auth_token =  config('OTP_TWILIO_AUTH_TOKEN')
verify_sid =  config('VERIFY_SID')
verified_number = config('VERIFIED_NUMBER')


client = Client(account_sid, auth_token)

verification = client.verify.v2.services(verify_sid) \
  .verifications \
  .create( to=verified_number, channel="sms")
print(verification.status)


otp_code = input("Please enter the OTP:")
# Custom message to be sent as the verification


verification_check = client.verify.v2.services(verify_sid) \
  .verification_checks \
  .create(to=verified_number, code=otp_code)

print(verification_check.status)



#
# from twilio.rest import Client
# from restaurants.settings.base import *
#
#
#
# account_sid = "ACfd02c7663f60f24c7693a793a7cb5747"
# # Your Auth Token from twilio.com/console
# auth_token  = "96f2ae65623319c74acc828bcedf4608"
#
# client = Client("ACfd02c7663f60f24c7693a793a7cb5747", "96f2ae65623319c74acc828bcedf4608")
#
# message = client.messages.create(
#     to='+916361233478',
#     from_= "+14178526828",
#     body="Hello from Mysore Resturant,this is the OTP")
#
# print(message.sid)
