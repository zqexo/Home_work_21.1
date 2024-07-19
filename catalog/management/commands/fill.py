from django.core.management import BaseCommand

from catalog.models import Student


class Command(BaseCommand):

    def handle(self, *args, **options):
        student_list = [
            {"last_name": "Petrov", "first_name": "Ivan"},
            {"last_name": "Ivanov", "first_name": "Petr"},
            {"last_name": "Петров", "first_name": "Иван"},
            {"last_name": "Иванов", "first_name": "Петр"},
        ]

        # for student_item in student_list:
        #     Student.objects.create(**student_list)

        students_for_create = []
        for student_item in student_list:
            students_for_create.append(Student(**student_item))

        Student.objects.bulk_create(students_for_create)
