from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
import pandas as pd  

# Building/Training model 
Emails = ["bafake5232@decodewp.com","brightsky39@emailondeck.com","vortex.mirror@fakeinbox.com","nightowl921@moakt.cc","zenpanda456@guerrillamail.com","coolcloud888@10minutemail.com","flashyduck01@trashmail.com","lunarwave21@temp-mail.org","greenowl77@dropmail.me","fastfox932@maildrop.cc"
          "davishunterboy@gmail.com","hunterdavis@uagateway.org","daishadavis1998@gmail.com","gryphonnevermind@gmail.com","info@centercourtclub.com","resources@hjtep.org","xiaoxiaolong.crystal@gmail.com","Seijifank@gmail.com","ellyh@cpe2.org","qteepie1212@aol.com","Budzeyday@aol.com","laura.brown@meditechgroup.com", "user9321@guerrillamail.com","test8823@temp-mail.org","guest1145@10minutemail.com","demo7432@dropmail.me","mailbot6590@maildrop.cc","emily.johnson94@gmail.com","michael.brooks21@yahoo.com","sarah.taylor@outlook.com","daniel.martinez83@hotmail.com","laura.nguyen01@gmail.com"]
labels = [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0]


v = CountVectorizer()
x = v.fit_transform(Emails)

x_train,x_test,y_train,y_test = train_test_split(x,labels,test_size= 0.01)

model = DecisionTreeClassifier() 
model.fit(x_train,y_train)

prediction = model.predict(x_test)
print("Accuracy",accuracy_score(y_test,prediction))
print("--------------------Test Compete------------------------")

newEmailVector = v.transform(["DspignerDavis@gmail.com"])#EAMPLE EMAIL
predictions = model.predict(newEmailVector)
print(predictions)

input()#BREAK TO TALK 

# Sorting my  data 
myData = pd.DataFrame(pd.read_csv("/Users/huntergoat/Downloads/Csv for Capstone project - Sheet1.csv"))
EmailVector = v.transform(myData['Email'])
filtering = model.predict(EmailVector)
myData['Spam Dection'] = filtering
filtering = myData[myData['Spam Dection'] ==0 ]
print(filtering)
filtering.to_csv("/Users/huntergoat/Downloads/Capstone Project.csv")


# Class Data
classData = pd.DataFrame(pd.read_csv("/Users/huntergoat/Downloads/capstoneDataFrame - Sheet1.csv"))
EmailVector1 = v.transform(classData['Email'])
filtering1 = model.predict(EmailVector1)
classData['Spam Dection'] = filtering1
filtering1 = classData[classData['Spam Dection'] ==0 ]
print(filtering1)
filtering1.to_csv("/Users/huntergoat/Downloads/Capstone Project (Data Given).csv")

