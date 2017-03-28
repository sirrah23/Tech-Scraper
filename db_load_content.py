from datetime import *
from sqlalchemy import *
from retrieve import HNParser, REDParser

# Connect to the database
engine = create_engine('mysql://sirrah:password@localhost/webdata?charset=utf8', encoding='utf-8')
conn = engine.connect()
metadata = MetaData()

# Initialize database table
webcontent = Table('webcontent', metadata,
    Column('content_id', Integer, primary_key=True),
    Column('title', String(500)),
    Column('link', String(500)),
    Column('source', String(50)),
    Column('inserted_at', DateTime, default=datetime.utcnow),
    Column('comment_link', String(500))
)
metadata.create_all(engine)

# Initialize data gathering objects
hnp = HNParser()	# Gets data from hacker news
redp = REDParser()	# Gets data from reddit

# Get content from web pages
# TODO: Catch RequestException at some point
content = hnp.content_arr()
content.extend(redp.content_arr())

# Initialize an insertion query
ins = webcontent.insert()

# Insert the content obtained from web pages into database
now = datetime.utcnow()
for item in content:
	conn.execute(ins, 
		title=item['title'], 
		link=item['link'], 
		source=item['source'], 
		inserted_at=now, 
		comment_link=item['comment_link'])

sel = webcontent.select()
rs = conn.execute(sel)
row = rs.fetchone()
# for row in rs:
#     print row.title, row.link

# Close connections when done
rs.close()
conn.close()