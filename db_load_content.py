from datetime import *
from sqlalchemy import *
import os
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
    Column('comment_link', String(500)),
    Column('is_favorite', Boolean, default=False)
)
metadata.create_all(engine)

# Initialize data gathering objects
hnp = HNParser()	# Gets data from hacker news
redp = REDParser(os.environ["REDDIT_USERNAME"])	# Gets data from reddit

# Get content from web pages
# TODO: Catch RequestException at some point
content = hnp.content_arr()
content.extend(redp.content_arr())

# Initialize an insertion query
ins = webcontent.insert()

# Insert the content obtained from web pages into database
# TODO: Filter out zero width spaces \u200\b (#&8203)
now = datetime.utcnow()
for item in content:
        try:
            conn.execute(ins,
                    title=item['title'],
                    link=item['link'],
                    source=item['source'],
                    inserted_at=now,
                    comment_link=item['comment_link'])
        except Exception as e:
            print e

sel = webcontent.select()
rs = conn.execute(sel)
row = rs.fetchone()

# Close connections when done
rs.close()
conn.close()
