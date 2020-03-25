from google.cloud import firestore

db = firestore.Client()


def insert_name(user_id, name):
    db.collection('key_owners').document('names').update({str(user_id): str(name)})


def delete_name(user_id):
    db.collection('key_owners').document('names').update({str(user_id): firestore.DELETE_FIELD})


def get_key_owners():
    owners = db.collection('key_owners').document('names').get()
    return owners


def get_allowed_groups():
    allowed_groups = db.collection('allowed_groups').document('chat_id').get()
    return allowed_groups
