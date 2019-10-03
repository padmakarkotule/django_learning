import datetime
import time
import jwt

jwt_payload = jwt.encode({
    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5),}, 'secret')



# JWT payload is now expired
# But with some leeway, it will still validate
time.sleep(3)
jwt_verify = jwt.decode(jwt_payload, 'secret', leeway=5)
#jwt_verify = jwt.decode(jwt_payload, 'secret')
if jwt_verify:
    print("Valid token")

time.sleep(3)
#jwt_verify = jwt.decode(jwt_payload, 'secret')
"""
leeway 
PyJWT also supports the leeway part of the expiration time definition, 
which means you can validate a expiration time which is in the past but not very far. 
For example, if you have a JWT payload with a expiration time set to 30 seconds after 
creation but you know that sometimes you will process it after 30 seconds, you can set 
a leeway of 10 seconds in order to have some margin
"""
jwt_verify = jwt.decode(jwt_payload, 'secret', leeway=5)
if jwt_verify:
    print("Valid token")

time.sleep(32)
jwt_verify = jwt.decode(jwt_payload, 'secret')
if jwt_verify:
    print("Valid token")