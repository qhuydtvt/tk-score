import mongoengine

#mongodb://<dbuser>:<dbpassword>@ds163176.mlab.com:63176/tk-score

host = "ds163176.mlab.com"
port = 63176
db_name = "tk-score"
user_name = "admin"
password = "admin"


def mlab_connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())