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
            self.__categories = data['props']['pageProps']['initialState']['init']['categories']
            self.__courses = data['props']['pageProps']['initialState']['init']['courses']
            self.__instructors = data['props']['pageProps']['initialState']['init']['instructors']
        except Exception as e:
            raise Exception('Something went worng with Ineuron Website!!!')

    def getCoursesMetadata(self):
        self.__scrapHomePage()
        coursesByCategory = {}
        for key, value in self.__courses.items():
            value['title'] = key
            if(value['categoryId'] in coursesByCategory):
                coursesByCategory[value['categoryId']].append(value)
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
            course = data['props']['pageProps']['data']
            instructors = data['props']['pageProps']['initialState']['init']['instructors']
            courseInstructor = course['meta']['instructors']
            courseInstructorDetails = {}
            for instruc in courseInstructor:
                courseInstructorDetails[instruc] = instructors[instruc]
            course['meta']['instructordetails'] = courseInstructorDetails
            return course
        except Exception as e:
            raise Exception('Something went worng with Ineuron Website!!!')

if __name__ == '__main__':
    obj = ScrapIneuron()
    pdf = CoursePDF()
    # obj.getCourseDetails('Full-Stack-Web-Development-with-Python-in-Hindi-Tech-Neuron')
    pdf.generateCoursePdf(obj.getCourseDetails('Full-Stack-Web-Development-with-Python-in-Hindi-Tech-Neuron'))