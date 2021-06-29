from jira import JIRA
import collections
import configparser

# Token=<your github access token>
config = configparser.ConfigParser()
config.read('.credentials')

jira = JIRA(basic_auth=(config['DEFAULT']['JIRA_USER'], config['DEFAULT']['JIRA_TOKEN']), options={'server':config['DEFAULT']['SERVER']})

query = 'project = IAM and resolution = Done AND assignee not in (Unassigned) AND resolutiondate < -30d'
resolved = jira.search_issues(query)

assignees = map(lambda issue : issue.fields.assignee.displayName, resolved)
occurs = collections.Counter(list(assignees))

print("Jiras resolved per Assignee in last 30 days:")
for name_count in sorted(occurs.items(), key=lambda pair: pair[1], reverse=True):
  print('{}:\t{}'.format(name_count[0], name_count[1]))
