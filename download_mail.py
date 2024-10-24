import imaplib
import email
import mailbox
import argparse
import getpass
import os

def download_emails(server, username, password, mailbox='INBOX', \
                     localfolder='emails.mbox', protocol='imap', output_format='mbox'):
    
    mail = imaplib.IMAP4_SSL(server)
    mail.login(username, password)
    mail.select("mailbox")
    result, data = mail.search(None, 'ALL')
    #list of email IDs
    email_ids = data[0].spli()

    if output_format == 'mbox':
        mbox = mailbox.mbox(localfolder)
        for email_id in email_ids:
            result, message_data = mail.fetch(email_id, "(RFC822)")
            raw_email = message_data[0][1]

            #Create an email message obj
            email_message = email.message_from_bytes(raw_email)

            mbox.add(email_message)

        mbox.flush()
        mbox.close()
        print("all email has been saved to  'emails.mbox")
    else:
        # create folder if need
        if not os.path.exists(localfolder):
            os.makedirs(localfolder)

        for email_id in email_ids:
            result, message_data = mail.fetch(email_id, "(RFC822)")
            raw_email = message_data[0][1]

            #Create an email message obj
            email_message = email.message_from_bytes(raw_email)

            #save email to file
            with open(os.path.join(localfolder, f'{email_id}.eml'), 'wb') as f:
                f.write(raw_email)

        print("All emails to 'emails' folder as eml files")
    mail.logout()


def main():
    parser = argparse.ArgumentParser(description='Download emails and save them in the specified format.')
    parser.add_argument('--server', required=True, help='IMAP server address (e.g., imap.gmail.com)')
    parser.add_argument('--user', required=True, help='Email username')
    parser.add_argument('--format', choices=['eml', 'mbox'], default='eml', help='Output format (eml or mbox)')

    args = parser.parse_args()

    # Prompt for password securely
    password = getpass.getpass(prompt='Password: ')

    download_emails(args.server, args.user, password, args.format)

if __name__ == '__main__':
    main()