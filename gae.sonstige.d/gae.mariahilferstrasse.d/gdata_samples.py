import pickle
import gdata.spreadsheet.text_db

client = gdata.spreadsheet.text_db.DatabaseClient()
client.SetCredentials('wolfgang.schuessel','iybnrxaseld')
#client.SetCredentials('ohramweltgeschehen','kidman')

databases=client.GetDatabases(name='imported-from-query')
tables=databases[0].GetTables(name='mhs')
target=tables[0]
source=tables[1]

print 'target table is ' + target.name 
print 'source table is ' + source.name 

databases=client.GetDatabases(name='geo20080813')
db=databases[0]

tables=db.GetTables(name='')
table=tables[0]
records=table.GetRecords(1,100)
print [r.content for r in records]
print [r.content for r in records if r.content['pickled']!=None]
ap=[r.content['pickled'] for r in records]
print len(ap)
print ap
au=[pickle.loads(i) for i in ap]
print au
#['', '', {'test': 'true', 'name': 'show'}, '', {'hausnummer': 5, 'has_content': False}, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', {'items': {'lokal': 'Asia Cooking'}, 'wifi': True}, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
print len(au)
#50
for i in range(0,len(au)):
    print i,au[i]
print records[30].content
#{'fundstelle': 'TRUE', 'hausnummer': '31', 'pickled': "(dp0\nS'items'\np1\n(dp2\nS'lokal'\np3\nS'Asia Cooking'\np4\nssS'wifi'\np5\nI01\ns.", 'address': 'mariahilferstrasse 31 wien', 'name': 'mhs:31'}
 
