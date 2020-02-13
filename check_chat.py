from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup


def get_credentials():
    with open("./credentials.json") as json_data_file:
        return json.load(json_data_file)
    return None


def init_selenium():
    webdriver_name = "./chromedriver"
    driver = webdriver.Chrome(webdriver_name)
    return driver


def authenticate(driver):
    credentials = get_credentials()
    driver.get(
        "https://auth.udacity.com/sign-in?next=https://classroom.udacity.com/authenticated")

    elem = driver.find_element(By.XPATH, "//input[@data-cy='signin-email']")
    elem.click()
    elem.send_keys(credentials["udacity"]["username"])

    elem = driver.find_element(By.XPATH, "//input[@data-cy='signin-password']")
    elem.click()
    elem.send_keys(credentials["udacity"]["password"])

    elem = driver.find_element_by_class_name(
        "button_primary__1qhjh")
    elem.click()

    # TODO: wait for something to appear on window instead of sleep
    time.sleep(10)
    # driver.implicitly_wait(10)
    return driver


def scrapp_student_hub(driver):

    # driver.get("https://hub.udacity.com/conversations/community:personal-mentor:nd019:en-us:u91114-11453659300?contextType=profile&profileId=11453659300")
    # time.sleep(5)
    # return None
    driver.get(
        "https://hub.udacity.com/")
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html5lib')

    # div for students chats: lobby-list_conversationsListInner__1-5Jx
    # get the <a> inside <li> inside that div, get url and parse for the
    # URL: href="/conversations/community:personal-mentor:nd019:en-us:u91114-11453659300?contextType=room

    # conversation-container_messageList__1zpZd

    direct_msgs_div = soup.find(
        "div", {"class": "lobby-list_conversationsListInner__1-5Jx"})
    if direct_msgs_div:
        chat_lis = direct_msgs_div.find_all("li")
        chat_urls = []
        for chat_li in chat_lis:
            chat_url = chat_li.find_all(
                "a", {"class": "lobby-list-item_roomListItem__1Abha"})
            chat_urls.append(chat_url[0]["href"])

        # TODO: Loop and read from every message chat
        driver.get("https://hub.udacity.com"+chat_urls[1])
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        chat = soup.find(
            "div", {"class": "conversation-container_messageList__1zpZd"})
        print("chat: ", chat)
        chat_blocks = chat.find_all(
            "ul", {"class": "message-list_dayBlock__1Oh9d"})
        print("chat_blocks: ", chat_blocks)
        for chat_block in chat_blocks:
            # each element has a data-day-block data-type to see that block date
            print("chat_block: ", chat_block)

            chat_user_title = chat_block.find(
                "div", {"class": "user-message_container__iNMoH"})
            title_a = chat_user_title.find("a", {"class": "vds-link"})
            print("title_a: ", title_a)

            # <div class = "user-message_header__3HG5Y" >
            #    <div class = "user-message_name__WSQPs" >
            #        <p class = "vds-text--sm vds-spacing--stack-none" >
            #             <a class = "vds-link" href = "#" > Carlos L. < /a >
            #         </p >
            #     </div >
            #     <span class = "badge_mentor__1JU7D badge_badge__3RgaW" >
            #         <i class = "vds-icon vds-icon--sm vds-color--cerulean" role = "img" aria-hidden="true">
            #            <svg viewBox = "0 0 32 32" >
            #                <path d = "M13 18H8v7a1 1 0 0 1-2 0V7.995C6 6.893 6.895 6 7.998 6h7.004C16.103 6 17 6.901 17 7.995V8h8a1 1 0 0 1 .857 1.514L23.167 14l2.69 4.486A1 1 0 0 1 25 20H14.996c-1.1 0-1.996-.901-1.996-1.995V18zm2-10v-.005C15 8 8 8 8 8v8.005c0-.003 2.931-.004 5-.005V9.995C13 8.893 13.893 8 14.996 8H15zm6.143 6.514a1 1 0 0 1 0-1.028L23.233 10H15v8.005C15 18 23.234 18 23.234 18l-2.091-3.486z" >
            #                 </path >
            #             </svg >
            #         </i >
            #         <span class = "badge_text__2j5se" >
            #             <p class = "vds-text--xs vds-spacing--stack-none" > Mentor</p>
            #         </span >
            #     </span >
            #     <p class = "vds-text--sm vds-color--silver vds-spacing--stack-none" >
            #         <time datetime = "2020-01-03T21:03:49.838332Z" title = "Fri Jan 03 2020 22:03:49 GMT+0100 (Central European Standard Time)">10:03 PM</time>
            #     </p >
            # </div >


def main():
    driver = init_selenium()
    driver = authenticate(driver)
    students = scrapp_student_hub(driver)


main()
