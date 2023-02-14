from flask import Flask, request
from flask_cors import cross_origin
from scrapIneuron import ScrapIneuron
from dbops import DBOps
from coursePdf import CoursePDF
from aws import AWS
import os

app = Flask(__name__)

os.environ['isReloadDataCalled'] = 'False'

def reload_data():
    os.environ['isReloadDataCalled'] = 'True'
    try:
        scrap = ScrapIneuron()
        dbOps = DBOps()
        crsPdf = CoursePDF()
        aws = AWS()
        courses = scrap.getAllCourses()
        dbOps.pushToMySQL(courses)
        dbOps.pushToMongoDB(courses)
        for crs in courses.keys():
            courseDetails = scrap.getCourseDetails(crs)
            pdfString = crsPdf.generateCoursePdf(courseDetails, savePdf=False)
            aws.uploadToS3(filePath = courseDetails.get('title'), pdfString=pdfString, isSavedPdf=False)
        os.environ['isReloadDataCalled'] = 'False'
    except Exception as e:
        print(e)

@app.route('/update-data', methods=['GET','POST'])
@cross_origin()
def update_data():
    if(request.method == 'GET'):
        if(os.environ['isReloadDataCalled'] == 'False'):
            reload_data()
            return 'successfull'
        else:
            return 'Process already running'

if __name__ == '__main__':
    app.run()