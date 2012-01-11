import tornado.ioloop
import tornado.web
import re
import sqlite3
import time
import json



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
        time real,
        lat real,
        lon real,
        accuracy real,
        altitude real)''')

        c = conn.cursor()
        # Insert a row of data
        c.execute('insert into trips values (null, %d, null)' %
                  (time.time()))
        print c.lastrowid
        trip_id = c.lastrowid

        res = c.execute('select * from waypoints')
        rows = []
        for row in res:
            rows.append(row)


        # We can also close the cursor if we are done with it
        c.close()


        self.render('routracker.html',
                    rows=rows,
                    trip_id=trip_id)

class WaypointHandler(tornado.web.RequestHandler):

    def post(self):
        data = json.loads(self.request.body)
        trip_id = data['trip_id']
        coords = data['position']['coords']

        conn = sqlite3.connect('/tmp/example')
        c = conn.cursor()

        c.execute('insert into waypoints values (%d, %d, %f, %f, %f, %f)' %
                  (trip_id, time.time(),
                   coords['latitude'],
                   coords['longitude'],
                   coords['accuracy'],
                   coords['altitude']))

        # Save (commit) the changes
        conn.commit()


        print self.request.body

        self.write('foo')


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/waypoint", WaypointHandler),
    ])

if __name__ == "__main__":
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()

