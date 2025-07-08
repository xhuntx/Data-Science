from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import pickle
import os.path
import email

# ========== STEP 1: ML Setup ==========
Emails = ["bafake5232@decodewp.com", "brightsky39@emailondeck.com", "vortex.mirror@fakeinbox.com",
          "nightowl921@moakt.cc", "zenpanda456@guerrillamail.com", "coolcloud888@10minutemail.com",
          "flashyduck01@trashmail.com", "lunarwave21@temp-mail.org", "greenowl77@dropmail.me",
          "fastfox932@maildrop.cc", "davishunterboy@gmail.com", "hunterdavis@uagateway.org",
          "daishadavis1998@gmail.com", "gryphonnevermind@gmail.com", "info@centercourtclub.com",
          "resources@hjtep.org", "xiaoxiaolong.crystal@gmail.com", "Seijifank@gmail.com", "ellyh@cpe2.org",
          "qteepie1212@aol.com", "Budzeyday@aol.com", "laura.brown@meditechgroup.com", "user9321@guerrillamail.com",
          "test8823@temp-mail.org", "guest1145@10minutemail.com", "demo7432@dropmail.me",
          "mailbot6590@maildrop.cc", "emily.johnson94@gmail.com", "michael.brooks21@yahoo.com",
          "sarah.taylor@outlook.com", "daniel.martinez83@hotmail.com", "laura.nguyen01@gmail.com"]

labels = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,0]
v = CountVectorizer()
x = v.fit_transform(Emails)
x_train, x_test, y_train, y_test = train_test_split(x, labels, test_size=0.01)

model = DecisionTreeClassifier()
model.fit(x_train, y_train)

# STEP 2: Gmail API Setup 
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
creds = None

if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
else:
    flow = InstalledAppFlow.from_client_secrets_file('/Users/huntergoat/Documents/Data Science /client_secret_667734235339-8dcrpkkbkpl15366mmemtqi6ls75mpcr.apps.googleusercontent.com.json', SCOPES)
    creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('gmail', 'v1', credentials=creds)

#  Read Recent Senders from Gmail 
results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=10).execute()
messages = results.get('messages', [])

email_list = []

for msg in messages:
    msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
    headers = msg_data['payload']['headers']
    for header in headers:
        if header['name'] == 'From':
            email_list.append(header['value'])

print("\nExtracted Email Senders from Gmail:")
for e in email_list:
    print("•", e)

#  Predict 
email_vectors = v.transform(email_list)
predictions = model.predict(email_vectors)

print("\n Email Classification Results:")
for email_addr, label in zip(email_list, predictions):
    print(f"{email_addr} => {'SPAM' if label == 1 else 'NOT SPAM'}")
