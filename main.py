import uvicorn, time, uuid, hashlib

from requests import Session

from Exception.handler import NotifyCallbackError

from fastapi.responses import RedirectResponse

from dotenv.main import dotenv_values

from fastapi import FastAPI, Response, Form

from urllib.parse import urlencode

from dotenv import load_dotenv

from typing import Optional



#-----------------------------------------------------#

app = FastAPI()

response = Response()

session = Session()

load_dotenv

config_env = dotenv_values(".env")    # ไฟล์ .env -> dict

#-----------------------------------------------------#
# Thanwa Chaleonyos

# ฟังก์ชันสำหรับ hash เพื่อทำ token state -> str
def getTokenState():

    hash_token_state = hashlib.sha512(
        str(uuid.uuid4().hex).encode('utf-8') +\
        str(time.time()).encode('utf-8')  
    ).hexdigest()

    return hash_token_state


@app.get('/authorize')
async def authorize():          
                                 # OAuth2 authorization endpoint URI ของ Line Notify
    authorize_notify_endpoint = 'https://notify-bot.line.me/oauth/authorize?{}&{}&{}'.format(
        urlencode({
            'response_type': 'code',    # fixed value ให้เป็น code เท่านั้น
            'client_id'    :  config_env['CLIENT_ID']   #client id 
        }), 
        f'redirect_uri={config_env["REDIRECT_URI"]}',  # ใส่ redirect uri ให้ตรงกับที่กรอก
        urlencode({
            'scope' : 'notify',     # fixed value ให้เป็น notify เท่านั้น
            'state' : getTokenState()   #เรียกใช้ฟังก์ชัน getTokenState() เพื่อป้องกัน CSRF ATK
        })
    )
    
    return RedirectResponse(url=authorize_notify_endpoint)
    

@app.get('/callback')
async def callback(code: str, state: str, error: Optional[str] = None, error_description: Optional[str] = None):
    try:
        if code and state :              #The OAuth2 token endpoint.
            session_post = session.post(url='https://notify-bot.line.me/oauth/token', 
            headers={
                'content-type' : 'application/x-www-form-urlencoded',
            },
            data={
                'grant_type' : 'authorization_code',   # fixed value ให้เป็น authorization_code
                'code' : code,
                'redirect_uri': config_env["REDIRECT_URI"],
                'client_id' : config_env["CLIENT_ID"],
                'client_secret' : config_env["CLIENT_SECRET"]     # Client secret
            })
            assert session_post.status_code == 200, session_post.status_code
            assert session_post.json()['status'] == 200, session_post.json()['status']     # check response status == 200?
        else:
            raise NotifyCallbackError('Callback error', error, error_description)
    except NotifyCallbackError as e:
        print(e.getMessage())
        return e

    except AssertionError as e:
        print('Bad request : ' ,e)
        return RedirectResponse(url='/authorize', status_code=e)

    # return RedirectResponse(url='<Your website>')
    # access_token อยู่ใน response body ซึ่งอยู่ในรูปแบบของ JSON Object. 
    return session_post.json()


#API สำหรับเช็ค สถานะของ access_token
@app.get('/check/api/status')
async def check_status_access_token():
    try:
        session_get = session.get(url='https://notify-api.line.me/api/status', 
        headers={
            'Authorization': 'Bearer <Your-access_token>'
        })
        assert session_get.status_code == 200, {'status': session_get.status_code, 'message': session_get.json()['message']}
        print(session_get.json())
    except AssertionError as e:
        print(e)
        return session_get.json()
   
    return session_get.json()


#API สำหรัยยกเลิก access_token
@app.get('/revoke/api')
async def revoke_access_token():
        session_post = session.post(url='https://notify-api.line.me/api/revoke', 
        headers={
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer <Your-access_token>'
        })
        
        if session_post.status_code == 200:
            return {'status': session_post.json()['status'], 'message': session_post.json()['message']}
        elif session_post.status_code == 401:
            return {'status': session_post.json()['status'], 'message': session_post.json()['message']}
        else:
            return {'status': session_post.json()['status'], 'message': session_post.json()['message']}


#API สำหรับส่งข้อความผ่าน Line notify
@app.post('/sendtext')
async def send_text_from_form(message_text: str = Form(...)):
    try:
        print(message_text)
        session_post = session.post(url='https://notify-api.line.me/api/notify', 
        headers={
            'content_type' : 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer <Your-access_token>'
        },
        data={
            'message': message_text
        })
        assert session_post.status_code == 200, session_post.json()
    except AssertionError as e:
        print(str(e))
        return e
    return session_post.json()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80, debug=True)