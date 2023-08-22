from jira import JIRA
import collections
import configparser
from datetime import datetime
import pprint


import sys
 
# Token=<your github access token>
config = configparser.ConfigParser()
config.read('.credentials')

jira = JIRA(basic_auth=(config['DEFAULT']['JIRA_USER'], config['DEFAULT']['JIRA_TOKEN']), options={'server':config['DEFAULT']['SERVER']})

project = str(sys.argv[1])


#epics = jira.search_issues(query, maxResults=50, startAt=50)

def getStories(epic):
  query = '"Epic Link"={0}'.format(epic)
  #print(query)
  items = jira.search_issues(query, maxResults=False)
  return items

''' 
  get the earliest sprint start date for a sprint that a issue was resolved in:
  - get the start and end of the sprint
  - get the sprint the issue was resolved in
      sprintstart <= resolutiondate <= sprintend 
  - update epic start date with that sprint start date
      startdate = sprintstart < startdate? sprintstart: startdate
'''
def updateStartDate(start_date, item):

  sprints = item.raw['fields']['customfield_10115']
  if not sprints: return start_date

  resolution_date = datetime.strptime(item.fields.resolutiondate.split('T')[0], '%Y-%m-%d')

  for sprint in sprints:
    #print(sprint)
    if sprint['state'] == 'closed':
      sprint_start = datetime.strptime(sprint['startDate'].split('T')[0], '%Y-%m-%d')
      sprint_end = datetime.strptime(sprint['completeDate'].split('T')[0], '%Y-%m-%d')

      if sprint_start <= resolution_date and resolution_date <= sprint_end:
        start_date = sprint_start if sprint_start < start_date else start_date
        #print("{0} {1}".format(item.key, start_date))

  return start_date

'''
donePoints is now also getting start and end dates
'''
def donePoints(epic):
  items = getStories(epic)

  epic_start_date = datetime(2070, 1, 1, 0, 0)
  epic_end_date = datetime(1970, 1, 1, 0, 0)

  points = 0
  for item in items:
    #if item.fields.status == 'Done':
    if item.fields.resolutiondate:
      #print("{0}, {1}".format(item.key, item.fields.resolutiondate))
      resolution_date = datetime.strptime(item.fields.resolutiondate.split('T')[0], '%Y-%m-%d')
      if resolution_date > epic_end_date:
        epic_end_date = resolution_date

      epic_start_date = updateStartDate(epic_start_date, item)
      #print(epic_start_date.date())

      ## sum story points
      story_points = item.raw['fields']['customfield_10117']
      if (not story_points == None):
        points += story_points

  #print(enddate)
  return (points, epic_start_date, epic_end_date)

def sum(epics):
  for epic in epics:
    #print(epic)
    (points, start, end) = donePoints(epic)
    if points > 0:
      print("{0}, {1}, {2}, {3}".format(epic, points, start.date(), end.date()))


def scan():
  query = 'project = "{0}" AND issuetype = Epic and issue = "CONNECT-1600"'.format(project)
  epics = jira.search_issues(query, maxResults=False)
  sum(epics)
"""   while not epics.isLast:

  startAt = len(epics)
    epics = jira.search_issues(query, maxResults=50, startAt=startAt)
    print(startAt)
    print(epics.isLast)
    print(epics.total)
    print(epics.maxResults)

    startAt += len(epics)
    sum(epics) """

scan()