import pymysql
conn=pymysql.connect(host='localhost',  database='Car Detection project', user='root', password='')
myCursor=conn.cursor()
myCursor.execute("""CREATE TABLE `Detectedcars` ( `id` INT NOT NULL , `name` TEXT NOT NULL , `photo` BLOB NOT NULL  , PRIMARY KEY (`id`));""")
conn.commit()
conn.close()