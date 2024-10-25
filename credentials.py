def get_credentials():
    try:
        f = open("userinfo.txt", "r")
        content = f.readlines()
        ic_user = content[0].rstrip()
        ic_pw = content[1].rstrip()
        initials = content[2].rstrip()
        destiny_user = content[3].rstrip()
        destiny_pw = content[4].rstrip()
        email = content[5].rstrip()
        email_pw = content[6].rstrip()
        email_sig = content[7].rstrip()
        synetic_user = content[8].rstrip()
        synetic_pw = content[9].rstrip()
        num_of_emails = len(content) - 11
        emails = []
        for i in range(num_of_emails):
            emails.append(content[i+10].rstrip())
        boss_email = content[len(content)-1]
        f.close()
        return(ic_user, ic_pw, initials, destiny_user, destiny_pw, email, email_pw, email_sig, synetic_user, synetic_pw, emails, boss_email)
        
    except:
        f = open("userinfo.txt", "wt")
        ic_user = input("Enter your IC username: ")
        f.write(ic_user + "\n")
        ic_pw = input("Enter your IC password: ")
        f.write(ic_pw + "\n")
        initials = input("Enter your initials: ")
        f.write(initials + "\n")
        destiny_user = input("Enter your destiny username: ")
        f.write(destiny_user + "\n")
        destiny_pw = input("Enter your destiny password: ")
        f.write(destiny_pw + "\n")
        email = input("Enter your full email address: ")
        f.write(email + "\n")
        email_pw = input("Enter your email password: ")
        f.write(email_pw + "\n")
        email_sig = input("Enter your email signature (ex: ~Weston): ")
        f.write(email_sig + "\n")
        synetic_user = input("Enter your synetic username: ")
        f.write(synetic_user + "\n")
        synetic_pw = input("Enter your synetic password: ")
        f.write(synetic_pw + "\n")

        mail_to = input("Enter the email address of someone you need to email: ")
        emails = []
        while mail_to != "s":
            f.write(mail_to + "\n")
            emails.append(mail_to)
            mail_to = input("Enter another email or type s to stop: ")
        boss_email = input("Enter your boss' email address: ")
        f.write(boss_email)
        f.close()
        return(ic_user, ic_pw, initials, destiny_user, destiny_pw, email, email_pw, email_sig, synetic_user, synetic_pw, emails, boss_email)