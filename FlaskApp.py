from flask import Flask,request;

app=Flask(__name__)

@app.route('/api/v1/login',methods=['GET','POST'])
def verifyAuth():
    body=dict(request.json)
    # data validation
    if(len(body.keys())!=2):
        return {"cd":"001","sms":"number of param is not valid!","data":{}}
    if('uname' not in body.keys()):
        return {"cd": "002", "sms": "uname dose not exist!", "data": {}}

    if ('upass' not in body.keys()):
        return {"cd": "003", "sms": "upass dose not exist!", "data": {}}

    from flaskdemoo.model.loginmodel import LoginDto,LoginDao;
    dto=LoginDto();
    dto.Uname=body['uname']
    dto.Upass=body['upass']
    dao=LoginDao();
    result=dao.verifyAuth(dto)
    if(result==True):
        return {"cd":"000","sms":"success!","data":{}}
    else:
        return {"cd": "888", "sms": "not found!", "data": {}}

@app.route('/api/v1/confirm',methods=['GET','POST'])
def confirmCode():
    body=dict(request.json)
    # data validation
    if(len(body.keys())!=3):
        return {"cd":"001","sms":"number of param is not valid!","data":{}}
    if('uname' not in body.keys()):
        return {"cd": "002", "sms": "uname dose not exist!", "data": {}}

    if ('upass' not in body.keys()):
        return {"cd": "003", "sms": "upass dose not exist!", "data": {}}

    from flaskdemoo.model.loginmodel import LoginDto,LoginDao;
    dto=LoginDto();
    dto.Uname=body['uname']
    dto.Upass=body['upass']
    dto.ConfirmCode=body['confirm_code']
    dao=LoginDao();
    result=dao.confirmCode(dto)
    if(result==True):
        return {"cd":"000","sms":"success!","data":{}}
    else:
        return {"cd": "888", "sms": "not found!", "data": {}}


app.run(port=9089)