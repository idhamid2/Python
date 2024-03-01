# Script Name: script.py
# Description: Scripts used to filter new addresses from the file and check the postal code
#              and after that send email to the concerned person of the Stadt with new addresses
# Things to change: Kindly change the file paths in line-29 and line-93 and change/put your email line 111-113
# Date:        20-04-2022


import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# variable used to store the postal code of districts
postal_code = {"Alfter": 53347, "Bad-Honnef": 53604, "Bornheim": 53332, "Eitorf": 53783, "Hennef": 53773,
               "Koenigswinter": 53639, "Lohmar": 53797, "Meckenheim": 53340, "Kriegsdorf": 53844,
               "Much": 53804, "Neunkirchen-Seelscheid": 53819, "Niederkassel": 53859, "Rheinbach": 53359,
               "Ruppichteroth": 53809, "Müllekoven": 53844, "Oberlar": 53842, "Spich": 53842,
               "Sankt-Augustin": 53757, "Siegburg": 53721, "Wipperfürth": 51688,
               "Swisttal": 53913, "Troisdorf": 53840, "Friedrich-Wilhelms-Hütte": 53840, "Wachtberg": 53343,
               "Windeck": 51570, "Bergneustadt": 51702, "Rotter See": 53844, "Rotter-See": 53844,
               "Engelskirchen": 51766, "Gummersbach": 51643, "Hückeswagen": 42499, "Sieglar": 53844,
               "Lindlar": 51789, "Marienheide": 51709, "Morsbach": 51597, "Nümbrecht": 51588, "Radevormwald": 42477,
               "Reichshof": 51580, "Waldbröl": 51545, "Wiehl": 51674, "Altenrath": 53842, "Bergheim": 53844,
               "Eschmar": 53844}

# variable used to store the new addresses and streets in the form of object
new_data = []

# reading the data file to filter out new addresses and streets
with open('file.txt', encoding='utf8') as f:
    lines = f.readlines()
    i = 1
    linesLength = len(lines)
    current_datenbank_name = ""  # storing the district name
    current_table_name = ""  # storing the table name whether it is Address ot Streets
    while i < linesLength:
        if "Datenbank" in lines[i]:
            current_datenbank_name = (((lines[i]).split('"')[1]).split(' -')[0])
            if current_datenbank_name == "Neunk.-Seelsch.":
                current_datenbank_name = "Neunkirchen-Seelscheid"
            elif current_datenbank_name == "St. Augustin":
                current_datenbank_name = "Sankt-Augustin"
            elif current_datenbank_name == "Königswinter":
                current_datenbank_name = "Koenigswinter"
            elif current_datenbank_name == "Bad Honnef":
                current_datenbank_name = "Bad-Honnef"
            current_table_name = ((lines[i]).split('"')[3])
            i += 2
        elif "neu" in lines[i]:  # checking by condition if there is a "neu" word in the line
            if current_table_name == "Adressen":  # condition used to check if the current table is Adressen
                data_district_name = (lines[i + 8]).split('"')[1]
                data_postal_code = (lines[i + 7]).split('"')[1]

                if re.search(r"\s", data_postal_code):
                    data_postal_code = 0
                else:
                    data_postal_code = int(data_postal_code)

                if data_district_name in postal_code:  # comparing the postal code of the file with above stored list
                    data_postal_code = postal_code[data_district_name]
                elif current_datenbank_name in postal_code:
                    data_postal_code = postal_code[current_datenbank_name]

                # combing other fields to make complete address
                current_address = (lines[i + 2]).split('"')[1] + " " + (lines[i + 3]).split('"')[1] + " " + \
                                  (lines[i + 4]).split('"')[1] + (lines[i + 5]).split('"')[1] + " " + \
                                  str(data_postal_code) + " " + data_district_name
                # append the new address data to above defined variable.
                new_data.append(
                    {'Databanken': current_datenbank_name, 'Type': current_table_name, 'Data': current_address})
                i += 9
            # condition used to check if the the current table is StraBen
            elif current_table_name == "Straßen ":
                current_street = (lines[i + 2]).split('"')[1] + " " + (lines[i + 3]).split('"')[1] + " " + \
                                 (lines[i + 5]).split('"')[1] + " " + (lines[i + 6]).split('"')[1]

                # append the new address data to above defined variable.
                new_data.append(
                    {'Databanken': current_datenbank_name, 'Type': current_table_name, 'Data': current_street})
                i += 7
            else:
                i += 1
        else:
            i += 1

# printing the len of new data stored in variable.
print("Total length of new data is: " + str(len(new_data)))
print('Process of getting new data from the file has been completed')

# This section is used to send EMAIL with new Address/Streets Data

# variable used to store all required mail addresses
mail_adresses = []
with open("emails.txt") as adresses:  # change the file path
    for a in adresses:
        mail_adresses.append(a.split('\t')[1].strip('\n'))
print('Email-Addresses has been read from the file')

stadt_list = ["Alfter", "Bad-Honnef", "Bornheim", "Eitorf", "Hennef", "Koenigswinter", "Lohmar", "Meckenheim", "Much",
              "Neunkirchen-Seelscheid", "Niederkassel", "Rheinbach", "Ruppichteroth", "Sankt-Augustin", "Siegburg",
              "Swisttal", "Troisdorf", "Wachtberg", "Windeck"]

for stadt in stadt_list:
    send_email_address = ""
    for email_address in mail_adresses:
        if stadt in email_address or stadt.lower() in email_address:  # checking that stadt name exist in the email or not
            send_email_address = send_email_address + email_address + ";" # adding multiple email addressses for receiver

    if send_email_address:
        host = "host_domain"
        server = smtplib.SMTP(host)
        FROM = "test@xyz.com"
        TO = 'test@xyz.com'          

        # Adding the Subject to Email
        msg = MIMEMultipart()
        sub = 'Neue Straßen/Adressen in MESO/VOIS für AGK ' + stadt
        msg['Subject'] = sub

        # getting the required data for the  only/selected stadt from the new filtereed data
        email_new_data = ""
        for data in new_data:
            if data['Databanken'] == stadt:
                email_new_data = email_new_data + data['Data'] + '\n'

        if email_new_data != "":
            # making Email body text
            emailText = ("Sehr geehrte Damen und Herren,\n\n "
                         "unten angefügt befinden sich die wöchentliche(n) neue(n) Straße(n) und Adresse(n) "
                         "aus MESO/VOIS für AGK."
                         "Ich bitte Sie, diese (falls nicht bereits geschehen) in AGK zu ergänzen und sie der KRG u. den "
                         "Gebieten zuzuordnen.\n"
                         "Sie erhalten diese E-Mail nur, wenn es in Ihrer Kommune laut MESO/VOIS "
                         "min. eine neue Straße oder Adresse gibt. Bei Fragen können Sie sich gerne an mich wenden. \n\n\n"
                         + email_new_data + '\n\n'
                                            "Mit freundlichen Grüßen,\n")

            # Attaching the email body text to message object
            msg.attach(MIMEText(emailText, 'plain'))

            # sending the Email
            TEXT = msg.as_string()
            server.sendmail(FROM, TO, TEXT)

            server.quit()

            print('Email has been sent to ' + email_address)
