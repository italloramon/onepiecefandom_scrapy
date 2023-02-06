import psycopg2

from itemadapter import ItemAdapter

class OnepiecefandomScrapyPipeline:
    def __init__(self):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'postgres' # your password
        database = 'onepiecewiki'

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create characterswiki table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS characterswiki(
            id serial PRIMARY KEY, 
            name VARCHAR(255),
            chapter int,
            episode int,
            year int,
            note text
        )
        """)

    def process_item(self, item, spider):
        ## Define insert statement
        self.cur.execute(""" insert into characterswiki (name, chapter, episode, year, note) values (%s,%s,%s,%s,%s)""", (
            item["name"],
            int(item["chapter"]),
            int(item["episode"]),
            int(item["year"]),
            item["note"]
        ))

        ## Execute insert of data into database
        self.connection.commit()
        return item

    def close_spider(self, spider):
        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()
