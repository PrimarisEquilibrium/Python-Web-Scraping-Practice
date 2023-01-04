from bs4 import BeautifulSoup
import requests
import time


# Unfamiliar skill checker
unfamiliar_skills = []
print("Put skills you are not familiar with | (!! TYPE 'exit' TO EXIT LOOP)")
while True:
    item = input("> ").lower()
    if item == "exit":
        print("Generating jobs...")
        break

    unfamiliar_skills.append(item)
    print(f"Filtering out {item}")

def find_jobs():

    # HTML / Soup Initialization
    html_text = requests.get("https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=").text
    soup = BeautifulSoup(html_text, "lxml")

    # Webscrap lookup
    jobs = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")
    for index, job in enumerate(jobs):

        published_date = job.find("span", class_="sim-posted").span.text
        if "few" in published_date: continue

        skills = job.find("span", class_="srp-skills").text.replace(" ", "")
        for skill in skills.split(","):
            if skill.strip().lower() in unfamiliar_skills: continue

        company_name = job.find("h3", class_="joblist-comp-name").text
        company_name = " ".join(company_name.split())

        more_info = job.header.h2.a["href"]

        with open(f"posts/{index}__job_log.txt", "w") as f:
            f.write(f"Company Name: {company_name.strip()} \n")
            f.write(f"Required Skills: {skills.strip()} \n")
            f.write(f"More Info: {more_info}")
        print(f"File saved: {index}__job_log.txt")

if __name__ == "__main__":
    while True:
        find_jobs()
        time_wait = 10
        print(f"Waiting {time_wait} minutes...")
        time.sleep(time_wait * 60)