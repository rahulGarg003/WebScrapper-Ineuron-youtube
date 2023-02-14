import mysql.connector
from dotenv import load_dotenv
import os
import json
import pymongo

class DBOps():
    def __init__(self):
        try:
            load_dotenv()
            with open('./config/config.json') as f:
                self.__config = json.loads(f.read())
        except Exception as err:
            print(err)
            raise

    def pushToMySQL(self, data: dict):
        try:
            mysqldb = mysql.connector.connect(
                host=os.getenv('AWS_MYSQL_DB_HOSTNAME'),
                user=os.getenv('AWS_MYSQL_DB_USERNAME'),
                password=os.getenv('AWS_MYSQL_DB_PASSWORD')
            )
            cur = mysqldb.cursor()

            query = f"CREATE DATABASE IF NOT EXISTS {self.__config.get('MYSQL_DB_NAME')} DEFAULT CHARACTER SET = 'utf8mb4';"
            cur.execute(query)

            query = f"""CREATE TABLE IF NOT EXISTS {self.__config.get('MYSQL_DB_NAME')}.coursedata 
                        (
                            courseid VARCHAR(100)NOT NULL,
                            coursename VARCHAR(1000),
                            description LONGTEXT,
                            PRIMARY KEY (courseid)
                        )"""
            cur.execute(query)

            for key, values in data.items():
                courseTitle = key
                courseId = values.get('_id','')
                courseDescription = values.get('description','').replace('"',"'")

                query = f'''INSERT INTO 
                            {self.__config.get('MYSQL_DB_NAME')}.coursedata (courseid, coursename, description)
                            VALUES ("{courseId}","{courseTitle}","{courseDescription}")
                            ON DUPLICATE KEY UPDATE 
                            coursename = "{courseTitle}",
                            description = "{courseDescription}"
                        '''
                cur.execute(query)
            mysqldb.commit()
            mysqldb.close()
        except Exception as e:
            print(e)

    def pullFromMySQL(self):
        try:
            mysqldb = mysql.connector.connect(
                host=os.getenv('AWS_MYSQL_DB_HOSTNAME'),
                user=os.getenv('AWS_MYSQL_DB_USERNAME'),
                password=os.getenv('AWS_MYSQL_DB_PASSWORD')
            )
            cur = mysqldb.cursor()
            query = f"SELECT * FROM {self.__config.get('MYSQL_DB_NAME')}.coursedata"
            cur.execute(query)
            res = cur.fetchall()
            mysqldb.close()
            return res
        except Exception as err:
            print(err)

    def pushToMongoDB(self, courseData: dict):
        try:
            client = pymongo.MongoClient(os.getenv('MONGODB_ACCESS_URL'))
            db = client[self.__config.get('MONGO_DB_NAME')]
            coll = db['coursedata']
            for key, value in courseData.items():
                data = {'_id':key.replace(' ','-'), key:value}
                if (coll.count_documents({'_id' : key.replace(' ','-')})):
                    coll.update_one({'_id' : key.replace(' ','-')}, {'$set': {key:value}})
                else:
                    coll.insert_one(data)
        except Exception as err:
            print(err)

    def pullFromMongoDB(self, courseName: str):
        try:
            client = pymongo.MongoClient(os.getenv('MONGODB_ACCESS_URL'))
            db = client[self.__config.get('MONGO_DB_NAME')]
            coll = db['coursedata']
            courseName = courseName.replace(' ','-')
            res = coll.find_one({'_id' : courseName})
            return res
        except Exception as err:
            print(err)        

if __name__ == '__main__':
    db = DBOps()
    from scrapIneuron import ScrapIneuron
    # db.pushToMySQL(ScrapIneuron().getAllCourses())
    # db.pushToMongoDB(ScrapIneuron().getAllCourses())
    db.pullFromMongoDB('30-days-Fast-Track-Data-Science-Interview-Preparation')