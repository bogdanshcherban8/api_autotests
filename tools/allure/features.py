from enum import Enum


class AllureFeature(str, Enum):
    AUTHENTICATION = "Authentication"
    USERS = "Users"
    FILES = "Files"
    COURSES = "Courses"
    EXERCISES = "Exercises"