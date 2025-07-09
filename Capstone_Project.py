import tkinter as tk
from tkinter import scrolledtext
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import base64
import pickle
import os
import sys

# ==== Gmail API Scope ====
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# ==== ML Spam Classifier Setup ====
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
    "sarah.taylor@outlook.com", "daniel.martinez83@hotmail.com", "laura.nguyen01@gmail.com", "googlecloud@google.com"
]
labels = [1]*10 + [0]*11 + [1]*5 + [0]*7

v = CountVectorizer()
x = v.fit_transform(Emails)
x_train, x_test, y_train, y_test = train_test_split(x, labels, test_size=0.01)
model = DecisionTreeClassifier()
model.fit(x_train, y_train)

# ==== Gmail API Auth ====
def get_client_secret_path():
    if getattr(sys, 'frozen', False):
        # PyInstaller bundle
        return os.path.join(sys._MEIPASS, '/Users/huntergoat/Documents/Data Science /client_secret_667734235339-8dcrpkkbkpl15366mmemtqi6ls75mpcr.apps.googleusercontent.com.json')
    else:
        return os.path.abspath('/Users/huntergoat/Documents/Data Science /client_secret_667734235339-8dcrpkkbkpl15366mmemtqi6ls75mpcr.apps.googleusercontent.com.json')

def authenticate_gmail():
    global service
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(get_client_secret_path(), SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

# ==== Spam Detection + GUI Integration ====
def classify_emails():
    result_text.delete(1.0, tk.END)
    try:
        service = authenticate_gmail()
    except Exception as e:
        result_text.insert(tk.END, f"Auth Error: {e}\n")
        return

    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=10).execute()
        messages = results.get('messages', [])
    except Exception as e:
        result_text.insert(tk.END, f"Error accessing Gmail: {e}\n")
        return

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
            result_text.insert(tk.END, "→ Moved to SPAM folder.\n")

        result_text.insert(tk.END, "\n")

# ==== GUI Setup ====
root = tk.Tk()
root.title("Gmail Spam Classifier")
root.geometry("640x450")

frame = tk.Frame(root)
frame.pack(pady=10)

btn = tk.Button(frame, text="Scan Gmail Inbox", command=classify_emails, font=("Arial", 14))
btn.pack()

result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, font=("Courier", 10))
result_text.pack(pady=10)

root.mainloop()
