import tkinter as tk
from tkinter import scrolledtext
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import base64
import pickle
import os.path
import email

Emails = [
    "bafake5232@decodewp.com", "brightsky39@emailondeck.com", "vortex.mirror@fakeinbox.com",
    "nightowl921@moakt.cc", "zenpanda456@guerrillamail.com", "coolcloud888@10minutemail.com",
    "flashyduck01@trashmail.com", "lunarwave21@temp-mail.org", "greenowl77@dropmail.me",
    "fastfox932@maildrop.cc", "davishunterboy@gmail.com", "hunterdavis@uagateway.org",
    "daishadavis1998@gmail.com", "gryphonnevermind@gmail.com", "info@centercourtclub.com",
    "resources@hjtep.org", "xiaoxiaolong.crystal@gmail.com", "Seijifank@gmail.com", "ellyh@cpe2.org",
    "qteepie1212@aol.com", "Budzeyday@aol.com", "laura.brown@meditechgroup.com", "user9321@guerrillamail.com",
    "test8823@temp-mail.org", "guest1145@10minutemail.com", "demo7432@dropmail.me",
    "mailbot6590@maildrop.cc", "emily.johnson94@gmail.com", "michael.brooks21@yahoo.com",
    "sarah.taylor@outlook.com", "daniel.martinez83@hotmail.com", "laura.nguyen01@gmail.com", "googlecloud@google.com","notifications@instructure.com"
]

labels = [1]*10 + [0]*11 + [1]*5 + [0]*8
v = CountVectorizer()
x = v.fit_transform(Emails)
x_train, x_test, y_train, y_test = train_test_split(x, labels, test_size=0.01)
model = DecisionTreeClassifier()
model.fit(x_train, y_train)


SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
creds = None
service = None

def authenticate_gmail():
    global service
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            '/Users/huntergoat/Documents/Data Science /client_secret_667734235339-8dcrpkkbkpl15366mmemtqi6ls75mpcr.apps.googleusercontent.com.json', SCOPES
        )
        creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)

def classify_emails():
    authenticate_gmail()
    result_text.delete(1.0, tk.END)
    
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=35).execute()
    messages = results.get('messages', [])
    
    if not messages:
        result_text.insert(tk.END, "No emails found.\n")
        return

    email_list = []
    full_message_info = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_data['payload']['headers']
        sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown")
        email_list.append(sender)
        full_message_info.append((msg['id'], sender))
    
    vectors = v.transform(email_list)
    predictions = model.predict(vectors)

    for (msg_id, sender), label in zip(full_message_info, predictions):
        status = "SPAM" if label == 1 else "NOT SPAM"
        result_text.insert(tk.END, f"{sender} => {status}\n")

        if label == 1:
            service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'addLabelIds': ['SPAM'], 'removeLabelIds': ['INBOX']}
            ).execute()
            result_text.insert(tk.END, f"→ Moved to SPAM folder.\n")
        result_text.insert(tk.END, "\n")

root = tk.Tk()
root.title("Gmail Spam Classifier")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=10)

scan_btn = tk.Button(frame, text="Scan Inbox", command=classify_emails, font=("Arial", 14))
scan_btn.pack()

result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, font=("Courier", 10))
result_text.pack(pady=10)

root.mainloop()
