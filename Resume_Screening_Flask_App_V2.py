from flask import Flask
from flask import Flask, request , jsonify
#from werkzeug.utils import secure_filename
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
#from __future__ import unicode_literals, print_function
import plac
import random
import re
from pathlib import Path
import spacy
import sys, fitz
from tqdm import tqdm
nlp = None

app = Flask(__name__)
#run_with_ngrok(app)  # Start ngrok when app is run

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
############### load model and inference
#nl = spacy.load('C:/Users/inrra3/PycharmProjects/Resume_Screening/')

def load_model():
    global nlp
    nlp = spacy.load('C:/Users/inrra3/PycharmProjects/Resume_Screening/',disable=['parser', 'tagger', 'textcat'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_mobile_number(text):
    phone = re.findall(re.compile(
        r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'),
                       text)
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number


def extract_email(email):
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None


def extract_skills(text):
    for t in text:
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
    # print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
    return entities


@app.route('/resumesummary', methods=['GET', 'POST'])
def resume_screening():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            file.save('./user_file.pdf')

        doc = fitz.open('./user_file.pdf')
        text = ""
        for page in doc:
            text = text + str(page.getText())

        text = " ".join(text.split('\n'))
        text = re.sub(r'[^\x00-\x7F]+', ' ',text) #only ascii
        text = re.sub('[^0-9a-zA-Z ]+', " ", text) # Keeps only alphanumeric
        text = re.sub(' +', ' ', text) # replacing spaces to single space
        print(text)

        mobile = extract_mobile_number(text)
        email = extract_email(text)
        skills = extract_skills(text)

    return jsonify([mobile,email,skills])

@app.route('/resumesummarytext', methods=['GET', 'POST'])
def resume_screening_text():
    if request.method == 'POST':
        text = request.form['user_text']
        print(text)
        mobile = extract_mobile_number(text)
        email = extract_email(text)
        skills = extract_skills(text)

    return jsonify([mobile,email,skills])

if __name__ == "__main__":
    print(("* Loading model and Flask starting server..."
        "please wait until server has fully started"))
    load_model()
    app.run()



'''
load_model()
text = "Jyotirbindu Patnaik Associate consultant@SAP labs , Bangalore Karnataka  Bengaluru, Karnataka - Email me on Indeed: indeed.com/r/Jyotirbindu- Patnaik/77e3ceda47fbb7e4  - Experienced incident and change coordinator and strongly skilled and dedicated ITIL Expert with a superior work ethic and management satisfaction record. Widely and deeply knowledgeable in all aspects of ITIL management and coordination. Adept multitasker able to deal a very high priority complex situations with accuracy and professionalism.  Willing to relocate to: Bangalore, Karnataka  WORK EXPERIENCE  Associate consultant  Sap labs  Incident and change management coordinator, dealing with the escalation process of company products. Notifying the customer as well as stake holders regarding the on going issue as well as helping problem management team to provide RCA.  Associate consultant  Sap labs  - Joining date from: January 25, 2017 Designation: Associate Consultant Company: SAP on the payroll of Bristlecone India LTD.  Roles and responsibilities: - Incident Coordinator: 1. Following the escalation process and handling the high priority incidents by initiating the troubleshooting call and driving the entire call till the issue gets resolve. 2. Capturing the entire chronological order to provide the RCA for the unplanned downtimes. 3. As an incident coordinator, I was informing the internal stakeholders regarding the unplanned downtimes/high priority issue by sending the notifications periodically. 4. Post handling the issue we were updating the MTTR and monthly outage tracker to have a clear records of unplanned downtimes. 5. Monitoring the tools like Catchpoint, Pingdom, CSS for quick find of availability alerts and trying to troubleshoot by initial analysis ASAP. 6. Preparing the documents for all the new process and update it as per its new changes. 7. Providing the reports (KPI/Availability/IRT-MPT) on weekly and monthly basis to the management to minimize the number incidents. 8. I was analyzing regarding the number of incidents and alerts received, and providing the entire captured details to management for further process to reduce the incidents"

r = extract_skills(text)

'SKILLS' in r[0]


for i in r:
    if 'SKILLS' in i:
        print i
'''