import os
import extract_msg
import spacy
import re
from collections import Counter
import pandas as pd

pd.set_option('display.max_colwidth', None)

# Initialize spaCy model
nlp = spacy.load("fr_core_news_sm", disable=['ner', 'parser'])

# Directory containing the .msg files
directory_path = 'FOLDER_PATH'  # <-- Replace this with your directory path

all_emails = []

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.msg'):
        filepath = os.path.join(directory_path, filename)

        msg = extract_msg.Message(filepath)
        subject = msg.subject
        body = msg.body
        
        split_emails = re.findall(r"(De :.*?)(?=De :|$)", body, flags=re.DOTALL)
        
        # If split_emails is empty, skip this file and go to the next one
        if not split_emails:
            continue
        
        content = "\n".join(split_emails)

        # Extract From, Date, To, Subject from the latest email
        from_ = re.search(r"De : (.*?)\n", split_emails[0])
        sent_date = re.search(r"Envoyé : (.*?)\n", split_emails[0])
        to_ = re.search(r"À : (.*?)\n", split_emails[0])

        # List of words to exclude
        exclude_list = ["Envoyé", "Cc"]

        # List of days and months in French to exclude
        date_list = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche", 
             "janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", 
             "septembre", "octobre", "novembre", "décembre"]

        # Process the content using spaCy
        doc = nlp(content)

        # Extract only verbs and nouns as keywords, excluding tokens with "@", symbols, specific words, and dates
        keywords = [token.text for token in doc if token.pos_ in ["NOUN", "VERB"] 
                    and not token.is_stop 
                    and "@" not in token.text 
                    and token.text.isalpha()]

        # Post-processing: directly remove unwanted keywords from the list
        keywords = [word for word in keywords if word.lower() not in exclude_list and word.lower() not in date_list]

        keywords_counter = Counter(keywords)
        top_keywords = [word[0] for word in keywords_counter.most_common(10)]

        all_emails.append({
            "From": from_.group(1) if from_ else "",
            "Sent Date": sent_date.group(1) if sent_date else "",
            "To": to_.group(1) if to_ else "",
            "Subject": subject,
            "Content": content,
            "Top Keywords": ", ".join(top_keywords)
        })

# Create a DataFrame from all emails
df = pd.DataFrame(all_emails)