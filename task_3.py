from datetime import datetime

def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            function_name = old_function.__name__
            arguments = f'args: {args}, kwargs: {kwargs}'
            log_entry = f"{timestamp} - {function_name} - {arguments} - result: {result}\n"
            with open(path, 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry)
            return result
        return new_function
    return __logger

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_finished_courses(self, course_name):
        self.finished_courses.append(course_name)

    def add_course_in_progress(self, courses_name):
        self.courses_in_progress.extend(courses_name)

    @logger('log.txt')
    def rate_lecture(self, lecturer_, course, rate):
        if isinstance(lecturer_, Lecturer) and course in self.courses_in_progress and course in lecturer_.courses_attached:
            if course in lecturer_.grades:
                lecturer_.grades[course] += [rate]
            else:
                lecturer_.grades[course] = [rate]
        else:
            return 'Ошибка'

    def average_score_hw(self):
        rate_list = []
        if self.grades:
            for value in self.grades.values():
                rate_list.extend(value)
            return sum(rate_list) / len(rate_list)
        return None

    def __eq__(self, other):
        return self.average_score_hw() == other.average_score_hw()

    def __lt__(self, other):
        return self.average_score_hw() < other.average_score_hw()

    def __le__(self, other):
        return self.average_score_hw() <= other.average_score_hw()

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {self.average_score_hw()}\n'
                f'Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n'
                f'Завершенные курсы: {', '.join(self.finished_courses)}')

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def add_course_attached(self, courses_name):
        self.courses_attached.extend(courses_name)

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    @logger('log.txt')
    def average_score_lecture(self):
        rate_list = []
        if self.grades:
            for value in self.grades.values():
                rate_list.extend(value)
            return sum(rate_list) / len(rate_list)
        return None

    def __eq__(self, other):
        return self.average_score_lecture() == other.average_score_lecture()

    def __lt__(self, other):
        return self.average_score_lecture() < other.average_score_lecture()

    def __le__(self, other):
        return self.average_score_lecture() <= other.average_score_lecture()

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {self.average_score_lecture()}')

class Reviewer(Mentor):

    @logger('log.txt')
    def rate_hw(self, student_, course, grade):
        if isinstance(student_, Student) and course in student_.courses_in_progress and course in self.courses_attached:
            if course in student_.grades:
                student_.grades[course] += [grade]
            else:
                student_.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}')

students_list = []
lecturers_list = []

student1 = Student('Севиров', 'Дмитрий', 'М')
students_list.append(student1)
student1.add_finished_courses('Выбор профессии')
student1.add_finished_courses('Введение в программирование')
student1.add_course_in_progress(['Python', 'Java'])

student2 = Student('Соколов', 'Роман', 'М')
students_list.append(student2)
student2.add_finished_courses('Введение в программирование')
student2.add_course_in_progress(['Python', 'C++'])

lecturer1 = Lecturer('Василий', 'Шабаров')
lecturers_list.append(lecturer1)
lecturer1.add_course_attached(['Python', 'C++'])

lecturer2 = Lecturer('Сергей', 'Веселов')
lecturers_list.append(lecturer2)
lecturer2.add_course_attached(['Python', 'Java'])

reviewer1 = Reviewer('Владимир', 'Красильников')
reviewer1.add_course_attached(['Python', 'C++'])
reviewer1.rate_hw(student1, 'Python', 8)
reviewer1.rate_hw(student2, 'Python', 6)

reviewer2 = Reviewer('Роман', 'Леонтьев')
reviewer2.add_course_attached(['Python', 'Java'])
reviewer2.rate_hw(student1, 'Python', 7)
reviewer2.rate_hw(student2, 'Python', 7)

student1.rate_lecture(lecturer1, 'Python', 9)
student2.rate_lecture(lecturer1, 'Python', 8)
student1.rate_lecture(lecturer2, 'Python', 8)
student2.rate_lecture(lecturer2, 'Python', 7)

@logger('log.txt')
def average_score_all_students(student_list, course_name):
    grades_list = []
    for student in student_list:
        if isinstance(student, Student) and course_name in student.courses_in_progress and course_name in student.grades:
            grades_list.extend(student.grades[course_name])
    print(f'Средняя оценка за домашние задания по всем студентам в рамках конкретного курса ({course_name}):')
    if grades_list:
        print(f'{sum(grades_list) / len(grades_list)}\n')
    else:
        print(f'Оценки по данному предмету отсутствуют\n')

@logger('log.txt')
def average_score_all_lecturers(lecturer_list, course_name):
    grades_list = []
    for lecturer in lecturer_list:
        if isinstance(lecturer, Lecturer) and course_name in lecturer.courses_attached and course_name in lecturer.grades:
            grades_list.extend(lecturer.grades[course_name])
    print(f'Среднея оценка за лекции всех лекторов в рамках конкретного курса ({course_name}):')
    if grades_list:
        print(f'{sum(grades_list) / len(grades_list)}\n')
    else:
        print(f'Оценки за данные лекции отсутствуют\n')