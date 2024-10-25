from label import *
from playwright.sync_api import sync_playwright
from datetime import date
from credentials import get_credentials

#pip list
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
            #page.click("#searchSidebar > ic-tool-context-search > div > div.flex-1.flex.flex-col.overflow-y-auto.ng-tns-c796485028-1.ng-star-inserted > section > ic-list-view > ul > li > ic-tool-context-search-result > button", timeout=20000)
            #page.click("#searchSidebar > ic-tool-context-search > div > div.flex-1.flex.flex-col.overflow-y-auto.ng-tns-c2871442543-1.ng-star-inserted > section > ic-list-view > ul > li > ic-tool-context-search-result > button", timeout=2000)
            page.get_by_text("#" + studentNum).click(timeout=2000)
        except:
            attempts += 1
            page.query_selector('//*[@id="undefined"]').click()
            if attempts < 5:
                open_student_page(attempts)


    page = context.new_page()
    page.goto('https://turnerusd202.infinitecampus.org/campus/turner.jsp')
    page.fill('#username', user_credentials[0])
    page.fill('#password', user_credentials[1])
    page.click('#signinbtn')

    page.get_by_label("Search").click()
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
    fullName = page.query_selector("#main-content > ic-title-bar-container > ic-title-bar > div > div.flex.flex-col.w-full.ng-tns-c3707218343-4 > div:nth-child(2) > ic-title-bar-selected-context-item > span").inner_text()
    #studentNum = page.query_selector("#main-content > ic-title-bar-container > ic-title-bar > div > div.flex.flex-col.w-full.ng-tns-c3707218343-4 > div:nth-child(2) > ic-title-bar-selected-context-item > ul > li:nth-child(1)").inner_text()
    grade = page.query_selector("#main-content > ic-title-bar-container > ic-title-bar > div > div.flex.flex-col.w-full.ng-tns-c3707218343-4 > div:nth-child(2) > ic-title-bar-selected-context-item > ul > li:nth-child(2)").inner_text()
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
    page1.click('#Login')
    page1.fill('#ID_loginName', user_credentials[3])
    page1.fill('#ID_password', user_credentials[4])
    page1.get_by_role("button", name="Log In").click()
    page1.get_by_role("link", name="Circulation").click()
    page1.get_by_role("link", name="Check In Items").click()
    page1.get_by_role("textbox").click()
    page1.get_by_role("textbox").fill(serialNumber)
    page1.get_by_role("button", name="Go!").click()
    page1.wait_for_selector('#blockTransactionList')

def complete_outlook():
    page2 = context.new_page()
    page2.goto('https://outlook.office.com/mail/')
    page2.get_by_placeholder("Email, phone, or Skype").click()
    page2.get_by_placeholder("Email, phone, or Skype").fill(user_credentials[5])
    page2.get_by_role("button", name="Next").click()
    page2.get_by_placeholder("Password").click()
    page2.get_by_placeholder("Password").fill(user_credentials[6])
    page2.get_by_role("button", name="Sign in").click()
    page2.get_by_role("button", name="Yes").click()
    #page2.locator("button").filter(has_text="New mailCreate a new email").click()
    page2.locator("button").filter(has_text="New mail").click()
    #add addresses to the to field
    for x in emailList:
        page2.get_by_label("To", exact=True).press_sequentially(x)
        page2.get_by_label(x).click()
    #add boss to the cc field
    page2.get_by_label("Cc", exact=True).press_sequentially(user_credentials[len(user_credentials)-1])
    page2.get_by_label(user_credentials[len(user_credentials)-1]).click()
    #fill in body
    page2.get_by_placeholder("Add a subject").fill(f"Damaged Device, {s1.initials}, {todaysDate}")
    page2.get_by_label("Message body, press Alt+F10").fill(f"{s1.name} - {reason}\n\n{user_credentials[7]}\n\n")
    page2.get_by_text("Draft saved").click()
    #page2.get_by_label("Favorites").get_by_text("Drafts").click()


def complete_synetic():
    page3 = context.new_page()
    page3.goto('https://synetic.repairportal.com/en/orders')
    page3.fill('#username', user_credentials[8])
    page3.fill('#password', user_credentials[9])
    page3.click('#ww > div > div > div > div > div:nth-child(3) > div > form > button')
    page3.get_by_text("Create new service order").click()
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


user_credentials = get_credentials()
emailList = user_credentials[10]
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

#using context manager to make browser close automatically
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    context = browser.new_context()
    s1 = complete_ic()
    #s1 = student(studentNum, "Man, Spider", "SM", "09", "Sp12345T28")
    complete_destiny()
    complete_outlook()
    if deviceType == "":
        complete_synetic()
    save_label(path, s1)
    print_label(path)
