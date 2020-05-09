# Add necesary import statements above
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize firebase app
cred = credentials.Certificate("hack-covid-19-e4018-firebase-adminsdk-pt6vv-e257520af7.json")
app = firebase_admin.initialize_app(cred)
# get reference to firestore
db = firestore.client()

###############################
# TODO: implement qr code reader using camera
###############################

# use this function to write the result of the test to the db
# result input should be a boolean value
def write_test_result_to_db(result):
    current_test = test_stand_data["tests"][-1] # most recent test will always be at the end of the array
    try:
        test_ref = db.collection("tests").document(current_test)
        test_ref.update({
            "result": result
        })
        return 1
    except:
        return 0


hard_coded_stand_id = "HrPMcrft5L0k4nH6MZNC"
qrcode_data = ""  # unlock code obtained from scanning qrcode
try:
    test_stand_ref = db.collection("test-stands").document(hard_coded_stand_id)
    test_stand_data = test_stand_ref.get().to_dict()
    if test_stand_data["unlockCode"] == qrcode_data:
        # TODO: implement functionality to run test using Alfie, and run write_test_result_to_db
        pass
    else:
        print("QR Code does not correspond to this testing stand. Please try again or verify that you are using the"
              "correct stand.")
        exit()
except:
    print("No such document")
