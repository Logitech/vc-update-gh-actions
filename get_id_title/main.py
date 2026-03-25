import os, re, requests

JIRA_URL = os.environ['JIRA_URL']
TEST_JIRA_URL = f"{JIRA_URL}rest/api/2/"
JIRA_TOKEN = os.environ["JIRA_TOKEN"]
headers = {
   'Authorization': f'Bearer {JIRA_TOKEN}',
   'Content-Type': 'application/json'
}
projects = os.environ['ALLOWED_PROJECTS']
title = os.environ['PR_TITLE']
jiras = re.findall(rf'\b(?:{projects})-\d+\b', title)
if (not jiras): 
    print(f'Jira ticket is not found in PR title. Error.')
    exit(1)

titles = []
for i, ticket in enumerate(jiras, 1):
    url = f"{TEST_JIRA_URL}issue/{ticket}"
    r = requests.get(url, headers=headers)
    print('Processing ' + ticket + ' ' + str(i) + '/' + str(len(jiras)))
    if not r.ok:
      print(f"No match for {ticket} at {JIRA_URL}")
      exit(1)
    details = r.json()
    if details is not None:
        if details['fields']['status']['name'] == "Done":
            print(f"Error: {ticket} is in resolved state")
            #exit(1)
        print(f'Jira ticket {ticket} is found. OK.')
    else:
        print(f'Jira ticket {ticket} is not found. Error.')
        exit(1)
    titles.append(details['fields']['summary'])    

github_output_path = os.getenv('GITHUB_OUTPUT')
with open(github_output_path, "a") as f:
    f.write(f"JIRA-IDS={'|,:'.join(jiras)}\n")
    f.write(f"JIRA-TITLES={'|,:'.join(titles)}\n")