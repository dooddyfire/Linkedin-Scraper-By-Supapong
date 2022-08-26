import datetime
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
#from linkedin_scraper import Person, actions
#Fix
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

start = time.time()

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


#code_set = [10221,14200,32309,10413,47912,64922,87909,28250,13129,84220]
keyword = input("ใส่ keyword : ")
filename = input("กรุณาใส่ชื่อไฟล์ : ")

username = 'xxxx@gmail.com'
passwordx = 'xxxx'
#n = int(input("ใส่จำนวนคนที่จะดึง : "))
driver = webdriver.Chrome(ChromeDriverManager().install())


#email = "kevinangas@gmail.com" # ใส่ username linkedin
#password = "Mikey131998" # ใส่ password linkedin
#actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal

main_url = "https://www.linkedin.com/search/results/people/?keywords={}%20engineer&origin=GLOBAL_SEARCH_HEADER&sid=%3Atn".format(keyword)
print(main_url)

driver.get("https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fsearch%2Fresults%2Fpeople%2F%3Fkeywords%3Dproduct%2520manager%2520engineer%26origin%3DGLOBAL_SEARCH_HEADER%26sid%3D%253Atn&fromSignIn=true&trk=cold_join_sign_in")
email = driver.find_element(By.XPATH,'//*[@id="username"]')
email.send_keys(username)

password = driver.find_element(By.XPATH,'//*[@id="password"]')
password.send_keys(passwordx)

login_btn = driver.find_element(By.XPATH,'//*[@id="organic-div"]/form/div[3]/button')
login_btn.click()

driver.get(main_url)


soup = BeautifulSoup(driver.page_source,'html.parser')

profile_link = list(set([i['href'] for i in soup.find_all('a',{'class':'app-aware-link'})][6:]))
print(profile_link)
print(len(profile_link))


card_mem = soup.find_all('div',{'class':'entity-result__content'})[6:]
current_work_lis = []
#for data in card_mem: 
#    try:
#        current_work = data.find('p',{'class':'entity-result__summary'}).text
#        print(current_work)
#        current_work_lis.append(current_work[current_work.find('at'):])
#    except: 
#        current_work = ""
#        print(current_work)
#        current_work_lis.append(current_work)     

image_lis = []


fname_lis = []
lname_lis = []
fullname_lis = []
head_lis = []
loc_lis = []

profile_link_lis = []
edu_lis = []
company_lis = []
all_skill_lis = []
time_study_lis = []
study_lis = []
all_exp_lis = []
all_exp_time_lis = []
degree_lis = []
for i in profile_link:
    print("url : ",i)
    driver.get(i)
    for t in range(0,3):
        driver.execute_script("window.scrollBy(0,5000)")
        time.sleep(2)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    try:
        fullname = soup.find('h1',{'class':'text-heading-xlarge'}).text.strip() 
        print(fullname)
        fullname_lis.append(fullname)
    except AttributeError: 
        continue
        fullname_lis.append("")

    try:
        firstname = fullname.split(" ")[0]
        print(firstname)
        fname_lis.append(firstname)
    except:
        continue
        fname_lis.append("")

    try:
        lastname = fullname.split(" ")[1]
        print(lastname)
        lname_lis.append(lastname)
    except:
        continue 
        lname_lis.append("")

    profile_link_lis.append(i)
    headline = soup.find('div',{'class':'text-body-medium'}).text.strip() 
    print(headline)
    head_lis.append(headline)

    loc = soup.find('div',{'class':'pb2'}).text.replace('Contact info',"").strip()
    print(loc)
    loc_lis.append(loc)

    image = soup.find('img',{'class':'pv-top-card-profile-picture__image'})['src']
    image_lis.append(image)
    print(image)


   
    for e in soup.find_all('section',{'class':'artdeco-card'}):
        if e.find('div',{'id':'education'}):  # Education
            all_edu = [ ed.text.strip()[:int(len(ed.text.strip())/2)]for ed in e.find_all('span',{'class':'mr1'})]
            print("all edu : ",all_edu)



            all_edu_time = [ edu.find('span',{'aria-hidden':'true'}).text for edu in e.find_all('span',{'class':'t-black--light'})  ]
            print("edu time : ",all_edu_time)
            all_edu_time_fix = []
            for edux in all_edu_time:  
                if all_edu_time.index(edux)%2 == 0:   
                    all_edu_time_fix.append(edux)
            print("all edu time fix : ",all_edu_time_fix)
   
            #bachelor degree
            try:
                degree_temp = []
                degree = [ c.find('span',{'class':'t-14'}).find('span',{'class':'visually-hidden'}).text for c in e.find_all('div',{'class':'justify-space-between'}) ]
                print('degree first ',degree)
                for dex in degree: 
                    try:
                        dx = int(dex[:4])
                        degree_temp.append(None)
                    except: 
                        degree_temp.append(dex)

                degree = degree_temp
            except AttributeError: 
                degree = None
            print('Degree : ',degree)
            


        if e.find('div',{'id':'experience'}):
            all_exp = [ ex.text.strip()[:int(len(ex.text.strip())/2)] for ex in e.find_all('span',{'class':'mr1'})]
            print(all_exp)


            all_exp_time = [ exp.find('span').text for exp in e.find_all('span',{'class':'t-black--light'})]
            print(all_exp_time) 
            
            #all_exp_time_fix = []
            #for expx in all_exp_time:  
            #    if all_exp_time.index(expx)%2 == 0:   
            #        all_exp_time_fix.append(expx)
            #print('exp time fix : ',all_exp_time_fix)


            all_exp_time_fix = []
            for expx in all_exp_time:  
                if has_numbers(expx) :   
                    all_exp_time_fix.append(expx)
            print('exp time fix : ',all_exp_time_fix)

        #driver.get(url+"details/skills/")
        #soupx = BeautifulSoup(driver.page_source,"html.parser")
        if e.find('div',{'id':'skills'}):
            all_skill = [ sk.text.strip()[:int(len(sk.text.strip())/2)] for sk in e.find_all('span',{'class':'mr1'})]
            print(all_skill)


    try:
        study_lis.append(all_edu)
        all_edu = " "
    except NameError:
        study_lis.append(" ")

    try:
        time_study_lis.append(all_edu_time_fix)
        all_edu_time_fix = " "    
    except NameError: 
        time_study_lis.append(" ")

    try:
        all_exp_lis.append(all_exp)
        all_exp = " "
    except NameError: 
        all_exp_lis.append(" ")

    try:
        all_exp_time_lis.append(all_exp_time_fix)
        all_exp_time_fix = " "
    except NameError: 
        all_exp_time_lis.append(" ")

    try:
        all_skill_lis.append(all_skill)
        all_skill = " "
    except NameError: 
        all_skill_lis.append(" ")

    try: 

        degree_lis.append(degree)

        degree = None
    except NameError:
        degree = None
        degree_lis.append(degree)
    # Final Check Value Lis 

    
    
    
    
    
    # Final Check Value Lis 
    

    #comp = soup.find('div',{'label':'Current company'}).text
    #company_lis.append(comp)
    #print(comp)

    #edu = soup.find('div',{'label':'Education'}).text
    #edu_lis.append(edu)
    #print(edu)
driver.close()
print(study_lis,len(study_lis))
print(time_study_lis,len(time_study_lis))
print(image_lis)
print(len(image_lis))
print("fname : ",len(fname_lis))
print("profile : ",len(profile_link[0:len(fname_lis)]))


print('url : ',len(profile_link_lis))
print('firstName : ',len(fname_lis))
print('lastname : ',len(lname_lis))
print('location : ',len(loc_lis))
print('headline : ',len(head_lis))
print('imgUrl : ',len(image_lis))
print('Education : ',len(study_lis))
print('Education Time : ',len(time_study_lis))
print('Experience : ',len(all_exp_lis))
print('Experience Time : ',len(all_exp_time_lis))
print('Skill: ',len(all_skill_lis))

df = pd.DataFrame()
df['Url_LinkedlnProfile'] = profile_link_lis
df['firstName'] = fname_lis
df['lastname'] = lname_lis
df['location'] = loc_lis
df['headline'] = head_lis 
df['imgUrl'] = image_lis
df['Skills'] = [ i for i in all_skill_lis] 
df['Education'] = [ i for i in study_lis] 
df['Education Time'] = [ i for i in time_study_lis]
df['Experience'] = [ i for i in all_exp_lis]
df['Experience Time'] =  [ i for i in all_exp_time_lis]




df['Degree'] = degree_lis
#df['Education'] = edu_lis 


df.to_excel("{}.xlsx".format(filename))




