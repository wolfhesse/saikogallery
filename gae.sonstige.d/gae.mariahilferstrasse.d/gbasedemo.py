
import gdata.base.service
import gdata.service
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import atom
import gdata.base

# Demonstrates queries to the snippets feed and stepping through the results.

gb_client = gdata.base.service.GBaseService()
q = gdata.base.service.BaseQuery()
q.feed = '/base/feeds/snippets'
q['start-index'] = '1'
q['max-results'] = '10'
q.bq = raw_input('Please enter your Google Base query: ')

feed = gb_client.QuerySnippetsFeed(q.ToUri())

while(int(q['start-index']) < 989):
  # Display the titles of the snippets.
  print 'Snippet query results items %s to %s' % (q['start-index'],
      int(q['start-index'])+10)
  for entry in feed.entry:
    print '  ', entry.title.text

  # Show the next 10 results from the snippets feed when the user presses
  # enter.
  nothing = raw_input('Press enter to see the next 10 results')
  q['start-index'] = str(int(q['start-index']) + 10)
  feed = gb_client.QuerySnippetsFeed(q.ToUri())

print 'You\'ve reached the upper limit of 1000 items. Goodbye :)'
