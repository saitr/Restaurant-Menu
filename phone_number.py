import phonenumbers

def validate_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if phonenumbers.is_valid_number(parsed_number):
            return True
        else:
            return False
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

phone_number = "+917892098558"
is_valid = validate_phone_number(phone_number)
if is_valid:
    print("Phone number is valid.")
else:
    print("Phone number is not valid.")
