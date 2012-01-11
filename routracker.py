import tornado.ioloop
import tornado.web
import re
import sqlite3
import time



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        conn = sqlite3.connect('/tmp/example')
        c = conn.cursor()
        # Create table
        c.execute('''create table if not exists trips
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time real,
        end_time real)''')

        c.execute('''create table if not exists waypoints
        (trip_id INTEGER,
        time real)''')

        c = conn.cursor()
        # Insert a row of data
        c.execute('insert into trips values (null, %d, null)' %
                  (time.time()))

        c.execute('insert into waypoints values (%d, %d)' %
                  (trip_id, time.time()))

        # Save (commit) the changes
        conn.commit()


        res = c.execute('select * from trips')
        rows = []
        for row in res:
            rows.append(row)

        # We can also close the cursor if we are done with it
        c.close()


        self.render('driver.html',
                    rows=rows)



application = tornado.web.Application([
    (r"/", MainHandler),
    ])

if __name__ == "__main__":
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()

