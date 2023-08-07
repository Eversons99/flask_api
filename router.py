from flask import Flask, request
from common import check_fields
from owner_modules import change_profile
import json

app = Flask(__name__)

@app.post("/alvocom/apply_commands")
def apply_commands():
    request_body = json.loads(request.data)
    verify_fields = check_fields.check_fields(request_body, 'alvocom')
    
    if ('error' in verify_fields.keys()):
        return verify_fields
    
    apply_reponse = change_profile.run(request_body)
    return apply_reponse



#RUN WITH PYTHON
"""
if __name__ == "__main__":
    app.run(host='10.0.30.244', port=8002, debug=True) 
"""


# RUN CLI: 
"""
    flask --app router run --host=10.0.30.244 --port=8002 --debug
    
"""