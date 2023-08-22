from jira import JIRA
import collections
import configparser
import pprint


import sys
 
# Token=<your github access token>
config = configparser.ConfigParser()
config.read('.credentials')

jira = JIRA(basic_auth=(config['DEFAULT']['JIRA_USER'], config['DEFAULT']['JIRA_TOKEN']), options={'server':config['DEFAULT']['SERVER']})

id = str(sys.argv[1])
priority = str(sys.argv[2]) if len(sys.argv) > 2 else ''


query = 'project = DOWN AND key = ' + id
resolved = jira.search_issues(query)
issue = resolved[0]
#print(resolved)
print(issue.fields.priority)
if (len(priority)):
    issue.update(fields={'priority': {'id': priority}})
    print(issue.fields.priority)

#issue.update(fields={'customfield_10484': {'completedCycles': {'startTime': 'Thursday 10:28 AM'}}})


"""
'customfield_10484': {
  'id': '14', 
  'name': 'Time to first response', 
  '_links': {
    'self': 'https://shippit.atlassian.net/rest/servicedeskapi/request/46723/sla/14'}, 
    'completedCycles': [{
      'startTime': {
        'iso8601': '2023-04-20T10:27:13+1000', 
        'jira': '2023-04-20T10:27:13.668+1000', 
        'friendly': 'Thursday 10:27 AM', 
        'epochMillis': 1681950433668}, 
      'stopTime': {
        'iso8601': '2023-04-20T11:00:44+1000', 
        'jira': '2023-04-20T11:00:44.227+1000', 
        'friendly': 'Thursday 11:00 AM', 
        'epochMillis': 1681952444227}, 
      'breachTime': {
        'iso8601': '2023-04-20T10:42:13+1000', 
        'jira': '2023-04-20T10:42:13.668+1000', 
        'friendly': 'Thursday 10:42 AM', 'epochMillis': 1681951333668}, 
      'breached': True, 
      'goalDuration': {
        'millis': 900000, 
        'friendly': '15m'}, 
      'elapsedTime': {
        'millis': 2010559, 
        'friendly': '33m'}, 
      'remainingTime': {
        'millis': -1110559, 
        'friendly': '-18m'}
    }], 
    'slaDisplayFormat': 'NEW_SLA_FORMAT'
  }
"""

""" assignees = map(lambda issue : issue.fields.assignee.displayName, resolved)
occurs = collections.Counter(list(assignees))

print("Jiras resolved per Assignee in last 30 days:")
for name_count in sorted(occurs.items(), key=lambda pair: pair[1], reverse=True):
  print('{}:\t{}'.format(name_count[0], name_count[1]))
 """