import requests
from bs4 import BeautifulSoup as bs
import json
from functools import reduce
from coursePdf import CoursePDF

class ScrapIneuron():
    def __scrapHomePage(self):
        try:
            url = 'https://www.ineuron.ai'
            rawdata = bs(requests.get(url).content, 'html.parser')
            data = json.loads(rawdata.find_all('script', id = '__NEXT_DATA__')[0].text)
            self.__categories = data.get('props',{}).get('pageProps',{}).get('initialState',{}).get('init',{}).get('categories',{})
            self.__courses = data.get('props',{}).get('pageProps',{}).get('initialState',{}).get('init',{}).get('courses',{})
            self.__instructors = data.get('props',{}).get('pageProps',{}).get('initialState',{}).get('init',{}).get('instructors',{})
        except Exception as e:
            raise Exception('Something went worng with Ineuron Website!!!')

    def getCoursesMetadata(self, byCategory = False):
        self.__scrapHomePage()
        if(byCategory):
            coursesByCategory = {}
            for key, value in self.__courses.items():
                value['title'] = key
                if(value.get('categoryId','') in coursesByCategory):
                    coursesByCategory.get(value['categoryId'],'').append(value)
                else:
                    coursesByCategory[value['categoryId']] = [value]
            return {"categories": self.__categories, "courses": self.__courses, "coursesByCategory": coursesByCategory, "instructor": self.__instructors}
        return {"categories": self.__categories, "courses": self.__courses, "instructor": self.__instructors}

    def getAllCourses(self):
        self.__scrapHomePage()
        return self.__courses

    def getCourseDetails(self, courseTitle :str):
        try:
            url = f"https://www.ineuron.ai/course/{courseTitle.replace(' ', '-')}"
            rawdata = bs(requests.get(url).content, 'html.parser')
            data = json.loads(rawdata.find_all('script', id = '__NEXT_DATA__')[0].text)
            courseData = data.get('props',{}).get('pageProps',{}).get('data',{})
            instructors = data.get('props',{}).get('pageProps',{}).get('initialState',{}).get('init',{}).get('instructors',{})
            courseInstructor = courseData.get('meta',{}).get('instructors',{})
            courseInstructorDetails = {}
            for instruc in courseInstructor:
                courseInstructorDetails[instruc] = instructors.get(instruc,{})
            courseData['meta']['instructordetails'] = courseInstructorDetails
            return courseData
        except Exception as e:
            raise Exception('Something went worng with Ineuron Website!!!')

if __name__ == '__main__':
    scrap = ScrapIneuron()
    crsPdf = CoursePDF()
    from aws import AWS
    # pdf.generateCoursePdf(obj.getCourseDetails('Automatic Number Plate Recognition'))
    # courses = scrap.getAllCourses()
    aws = AWS()
    # for crs in courses:
    #     pdf.generateCoursePdf(obj.getCourseDetails(crs))
    #     print(f"Pdf generateed for: {crs}")
    # courses = obj.getCoursesMetadata().get('courses').keys()
    # print(len(courses))
    # for crs in courses.keys():
    #     courseDetails = scrap.getCourseDetails(crs)
    pdfString = crsPdf.generateCoursePdf(scrap.getCourseDetails('Full-Stack-Data-Science-BootCamp-2.0'), savePdf=False)
    aws.uploadToS3(filePath = '123test', pdfString=pdfString, isSavedPdf=False)