from label import *
from playwright.sync_api import sync_playwright
from datetime import date
from credentials import get_credentials

#possible future additions
#regex validate asset, serial, stu number
#make it have a better framework
#fancy gui for it (select checkboxes with each thing, run again option)

class student:
    def __init__(self, number, name, initials, grade, password):
        self.number = number
        self.name = name
        self.initials = initials
        self.grade = grade
        self.password = password

    def __str__(self):
        return f"{self.number}\n{self.name}\n{self.initials}\n{self.grade}\n{self.password}"
    
def complete_ic():
    def open_student_page(attempts):
        try:
            page.get_by_placeholder("Student Search...").fill(studentNum, timeout=2000)
            page.get_by_placeholder("Student Search...").press("Enter", timeout=2000)
            page.get_by_text("#" + studentNum).click(timeout=2000)
        except:
            attempts += 1
            page.get_by_label("Search").first.click()
            if attempts < 5:
                open_student_page(attempts)


    page = context.new_page()
    page.goto('https://turnerusd202.infinitecampus.org/campus/turner.jsp')
    page.fill('#username', user_credentials[0])
    page.fill('#password', user_credentials[1])
    page.click('#signinbtn')

    page.get_by_label("Search").first.click()
    page.get_by_placeholder("Student Search...").fill(studentNum)
    page.get_by_placeholder("Student Search...").press("Enter")
    #for some reason search minimizes here, needs to be open in order to see next button to click
    open_student_page(0)

    page.get_by_role("link", name="Student Technology").click()
    oldComment = page.frame_locator("iframe[title=\"workspace\"]").frame_locator("iframe[name=\"frameWorkspace\"]").frame_locator("iframe[name=\"frameWorkspaceWrapper\"]").frame_locator("iframe[name=\"frameWorkspaceDetail\"]").get_by_role("textbox", name="Return Comments").text_content()
    page.frame_locator("iframe[title=\"workspace\"]").frame_locator("iframe[name=\"frameWorkspace\"]").frame_locator("iframe[name=\"frameWorkspaceWrapper\"]").frame_locator("iframe[name=\"frameWorkspaceDetail\"]").get_by_role("textbox", name="Return Comments").fill(f"{oldComment}\n{assetTag}, {serialNumber}, {reason}, {todaysDate} - {user_credentials[2]}")
    page.frame_locator("iframe[title=\"workspace\"]").frame_locator("iframe[name=\"frameWorkspace\"]").frame_locator("iframe[name=\"frameWorkspaceWrapper\"]").frame_locator("iframe[name=\"frameWorkspaceHeader\"]").get_by_role("link", name="Save").click()
    #ensure save has finished
    page.frame_locator("iframe[title=\"workspace\"]").frame_locator("iframe[name=\"frameWorkspace\"]").frame_locator("iframe[name=\"frameWorkspaceWrapper\"]").frame_locator("iframe[name=\"frameWorkspaceDetail\"]").get_by_role("textbox", name="Student Password").click()
    #get user info
    passw = page.frame_locator("iframe[title=\"workspace\"]").frame_locator("iframe[name=\"frameWorkspace\"]").frame_locator("iframe[name=\"frameWorkspaceWrapper\"]").frame_locator("iframe[name=\"frameWorkspaceDetail\"]").get_by_role("textbox", name="Student Password").input_value()
    fullName = page.query_selector('#main-content > ic-title-bar-container > ic-title-bar > div > div:nth-child(2) > div:nth-child(2) > ic-title-bar-selected-context-item > span').inner_text()
    #studentNum = page.query_selector("#main-content > ic-title-bar-container > ic-title-bar > div > div.flex.flex-col.w-full.ng-tns-c3707218343-4 > div:nth-child(2) > ic-title-bar-selected-context-item > ul > li:nth-child(1)").inner_text()
    grade = page.query_selector("#main-content > ic-title-bar-container > ic-title-bar > div > div:nth-child(2) > div:nth-child(2) > ic-title-bar-selected-context-item > ul > li:nth-child(2)").inner_text()
    grade = grade[7:]
    #trim off nicknames
    fullName = fullName.rstrip()
    if fullName[-1] == ")":
        while fullName[-1] != "(":
            fullName = fullName[:-1]
        fullName = fullName[:-2]
    #trim off mid initial
    if fullName[-2] == " ":
        fullName = fullName[:-2]
    initials = fullName[(fullName.index(",") + 2)] + fullName[0]
    return(student(studentNum, fullName, initials, grade, passw))

def complete_destiny():
    page1 = context.new_page()
    page1.goto('https://turnerusd202.follettdestiny.com')
    if user_credentials[-1] == "m":
        page1.get_by_text("Turner Middle School").click()
    else:
        page1.get_by_text("Turner High School").click()
    page1.click('#toolbar-guest-login-btn')
    page1.fill('#userName', user_credentials[3])
    page1.fill('#userPassword', user_credentials[4])
    page1.get_by_role("button", name="Log in", exact=True).click()
    page1.locator('#portal-spinner circle').nth(1).wait_for(state='visible')
    page1.locator('#portal-spinner circle').nth(1).wait_for(state='hidden')
    page1.click("#app-switch-button")
    page1.get_by_text("Back Office").click()
    page1.get_by_role("button", name="Circulation Circulation").click()
    page1.get_by_role("button", name="Check In Items", exact=True).click()
    page1.locator('[id="Library Manager"]').content_frame.locator("input[name='barcode']").click()
    page1.locator('[id="Library Manager"]').content_frame.locator("input[name='barcode']").fill(serialNumber)
    page1.locator('[id="Library Manager"]').content_frame.get_by_role("button", name="Go!").click()
    page1.locator('[id="Library Manager"]').content_frame.locator('#blockTransactionList').hover()

def complete_outlook():
    page2 = context.new_page()
    page2.goto('https://outlook.office.com/mail/')
    page2.get_by_placeholder("Email, phone, or Skype").click()
    page2.get_by_placeholder("Email, phone, or Skype").fill(user_credentials[5])
    page2.get_by_role("button", name="Next").click()
    page2.get_by_placeholder("Password").click()
    page2.get_by_placeholder("Password").fill(user_credentials[6])
    page2.get_by_role("button", name="Sign in").click()
    try:
        page2.get_by_role("button", name="Yes").click(timeout=5000)
    except:
        pass
    page2.get_by_role("button", name="New mail").first.click()
    #add addresses to the to field
    for x in emailList:
        page2.get_by_label("To", exact=True).press_sequentially(x)
        page2.locator("#FloatingSuggestionsItemId0").filter(has_text=x).click()
        #could have done page2.get_by_label("Last,First - lastf@") but then the user would have to enter the emails in a specific format that gets messy
    #add boss to the cc field
    page2.get_by_label("Cc", exact=True).press_sequentially(user_credentials[-2])
    page2.locator("#FloatingSuggestionsItemId0").filter(has_text=user_credentials[-2]).click()
    #fill in body
    page2.get_by_placeholder("Add a subject").fill(f"Damaged Device, {s1.initials}, {todaysDate}")
    page2.fill("#editorParent_1 > div > div", f"{s1.name} - {reason}\n\n{user_credentials[7]}\n\n")
    page2.keyboard.press("Control+s") #there is no save button, but this saves the draft
    page2.wait_for_timeout(3000) #this is just to make sure it gets enough time to save, unfortunately, theres no better way to check if it saved, so this is the best I can do
    

def complete_synetic():
    page3 = context.new_page()
    page3.goto('https://synetic.repairportal.com/en/orders')
    page3.fill('#username', user_credentials[8])
    page3.fill('#password', user_credentials[9])
    page3.click('#ww > div > div > div > div > div:nth-child(3) > div > form > button')
    page3.locator("#navbarLargeMenu").get_by_role("link", name="Create new service order").click()
    page3.get_by_label("Reference", exact=True).fill(assetTag)

    #page3.select_option('select#name','Macbook air') cant do this because then loading symbol never happens
    page3.click("#select2-name-container")
    page3.get_by_role("option", name="Macbook air").click()
    page3.locator('body > div.loader-container > div').wait_for(state='visible')
    page3.locator('body > div.loader-container > div').wait_for(state='hidden')

    page3.get_by_label('Serial number/IMEI').fill(serialNumber)
    page3.click('#issue')
    page3.locator('body > div.loader-container > div').wait_for(state='visible')
    page3.locator('body > div.loader-container > div').wait_for(state='hidden')

    page3.select_option('select#servicetype', 'Warranty service')
    page3.fill('#issue', f'{reason}')
    page3.select_option('select#product', 'On-Site Pickup')
    page3.select_option('select#delivery_out', 'Delivery')
    
    page3.click('#approve_button')
    #click something here to ensure you waited for it to load
    page3.get_by_text("You have chosen to ship the device").click()

def complete_worthave():
    page3 = context.new_page()
    page3.goto('https://www.worthavegroup.com/customer/account/login/')
    page3.get_by_role("textbox", name="Email").fill(user_credentials[10])
    page3.get_by_role("textbox", name="Password").fill(user_credentials[11])
    page3.get_by_role('button', name='Log In').click()
    page3.get_by_text('Claim Center').click()
    page3.get_by_role("textbox").fill(serialNumber)
    page3.locator("#yt_main").get_by_role("button", name="Search").click()
    page3.locator("#yt_main > div > div > div > div.loading-screen.fixed").wait_for(state='visible')
    page3.locator("#yt_main > div > div > div > div.loading-screen.fixed").wait_for(state='hidden')
    page3.get_by_text('File a claim', exact=True).click()
    page3.get_by_role('textbox').first.click()
    page3.get_by_text(str(date.today().strftime("%d")), exact=True).click()
    if reason == "Broken screen":
        page3.get_by_role("combobox").nth(1).select_option("140")
    elif 'battery' in reason.lower() or 'charge' in reason.lower():
        page3.get_by_role("combobox").nth(1).select_option("558")
    elif 'water' in reason.lower() or 'liquid' in reason.lower():
        page3.get_by_role("combobox").nth(1).select_option("158")
    else:
        page3.get_by_role("combobox").nth(1).select_option("137")
    page3.get_by_role("textbox").nth(1).fill(incidentDesc)
    page3.get_by_role("textbox").nth(2).fill(reason)
    page3.get_by_role("checkbox").check()
    page3.get_by_role("button", name="Submit").click()
    page3.get_by_text("Success Your claim for serial").click()


user_credentials = get_credentials()
emailList = user_credentials[12]
assetTag = input("Asset tag: ")
serialNumber = input("Serial num: ")
studentNum = input("Student num: ")
reason = input("Enter the type of break or for broken screen, press enter: ")
if reason == "":
    reason = "Broken screen"
deviceType = "unknown"
while deviceType != "" and deviceType != "i":
    deviceType = input("Enter i for intel device, or press enter for newer: ")
todaysDate = date.today().strftime("%m/%d/%y")
path = "student_label.jpg"
incidentDesc = reason
if serialNumber[:4].upper() == "FVFH" or serialNumber[:4].upper() == "FVFF":
    incidentDesc = input("Please describe how the device was damaged: ")

#using context manager to make browser close automatically
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    context = browser.new_context()
    s1 = complete_ic()
    #s1 = student(studentNum, "Man, Spider", "SM", "09", "Sp12345T28")
    complete_outlook()
    complete_destiny()
    if deviceType == "":
        if serialNumber[:4].upper() == "FVFH" or serialNumber[:4].upper() == "FVFF":
            complete_worthave()
        else:
            complete_synetic()
    save_label(path, s1)
    print_label(path)
