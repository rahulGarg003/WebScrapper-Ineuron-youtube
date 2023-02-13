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

    def getCoursesMetadata(self):
        self.__scrapHomePage()
        coursesByCategory = {}
        for key, value in self.__courses.items():
            value['title'] = key
            if(value.get('categoryId','') in coursesByCategory):
                coursesByCategory.get(value['categoryId'],'').append(value)
            else:
                coursesByCategory[value['categoryId']] = [value]
        return {"categories": self.__categories, "courses": coursesByCategory, "instructor": self.__instructors}

    def getListofCourses(self):
        self.__scrapHomePage()
        return list(self.__courses.keys())

    def getCourseDetails(self, courseTitle :str):
        try:
            url = f"https://www.ineuron.ai/course/{courseTitle.replace(' ', '-')}"
            rawdata = bs(requests.get(url).content, 'html.parser')
            data = json.loads(rawdata.find_all('script', id = '__NEXT_DATA__')[0].text)
            course = data.get('props',{}).get('pageProps',{}).get('data',{})
            instructors = data.get('props',{}).get('pageProps',{}).get('initialState',{}).get('init',{}).get('instructors',{})
            courseInstructor = course.get('meta',{}).get('instructors',{})
            courseInstructorDetails = {}
            for instruc in courseInstructor:
                courseInstructorDetails[instruc] = instructors.get(instruc,{})
            course['meta']['instructordetails'] = courseInstructorDetails
            return course
        except Exception as e:
            raise Exception('Something went worng with Ineuron Website!!!')

if __name__ == '__main__':
    obj = ScrapIneuron()
    pdf = CoursePDF()
    # pdf.generateCoursePdf(obj.getCourseDetails('Automatic Number Plate Recognition'))
    courses = obj.getListofCourses()
    # for crs in courses:
    #     pdf.generateCoursePdf(obj.getCourseDetails(crs))
    #     print(f"Pdf generateed for: {crs}")
    print(len(courses))