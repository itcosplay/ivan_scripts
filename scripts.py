from datetime import datetime
from random import choice

from datacenter.models import (
    Schoolkid,
    Teacher,
    Subject,
    Lesson,
    Mark,
    Chastisement,
    Commendation
)


def date_validate(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')

    except ValueError:
        print (
            'Неправильный формат даты!\n',
            'Необходимо ввести в формате ГГГГ-ММ-ДД',
            "пример для 11 марта 2021 года: '2021-03-11'"
        )

        return False

    return True


def find_schoolkid (
    schoolkid,
    year_of_study,
    group_letter
):
    '''
    Finds schoolkid from database
    '''
    try:
        schoolkid = Schoolkid.objects.get (
            full_name = schoolkid,
            year_of_study=year_of_study,
            group_letter=group_letter
        )

    except Schoolkid.MultipleObjectsReturned:
        print (
            f'Похоже, учеников {schoolkid} несколько...\n',
            'Проверьте правильность введённых ФИО\n',
            "пример: 'Иванов Иван Иванович'\n",
            'обязательно проверьте год обучения и букву класса\n',
            'чтобы исключить учеников из других классов'
        )

        return False

    except Schoolkid.DoesNotExist:
        print (
            'Такого ученика не существует!\n',
            'Проверьте правильность введённых ФИО\n',
            "пример: 'Иванов Иван Иванович'\n",
            'обязательно проверьте год обучения и букву класса'
        )

        return False
    
    return schoolkid


def fix_marks(
    schoolkid='Фролов Иван Григорьевич',
    year_of_study=6,
    group_letter='А'
):
    '''
    Changes bad grades (like 2 or 3) to perfect ones (5)
    in database
    '''
    schoolkid = find_schoolkid(schoolkid, year_of_study, group_letter)

    if schoolkid:
        Mark.objects.filter (
            schoolkid=schoolkid.id,
            points__in=[2,3]
        ).update(points=5)

        print (
            'Все двойки и тройки',
            'для ученика {schoolkid_name}'.format (
                schoolkid_name=schoolkid.full_name
            ),
            'исправленны на отлично!'
        )


def remove_chastisements(
    schoolkid='Фролов Иван Григорьевич',
    year_of_study=6,
    group_letter='А'
):
    '''
    Deletes chastisements for schoolkid
    '''
    schoolkid = find_schoolkid(schoolkid, year_of_study, group_letter)

    if schoolkid:
        Chastisement.objects.filter(schoolkid=schoolkid.id).delete()

        print(f'Все замечания для ученика {schoolkid} удалены успешно!')


def create_commendation(
    subject,
    date,
    schoolkid='Фролов Иван Григорьевич',
    year_of_study=6,
    group_letter='А'
):
    '''
    Creates new commendation for schoolkid from teacher.
    date = "YYYY-MM-DD"
    '''
    if date_validate(date) is False:

        return

    schoolkid = find_schoolkid(schoolkid, year_of_study, group_letter)

    if schoolkid is False:

        return

    try:
        lesson = Lesson.objects.get (
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
            subject__title=subject,
            date=date
        )
    except Lesson.MultipleObjectsReturned:
        print (
            'Проверьте правильность написания названия предмета,\n',
            'предмет должнен быть написан с большой буквы\n',
            'например Математика.'
        )

        return

    except Lesson.DoesNotExist:
        print (
            f'Занятия не обнаружено!'
            'Проверьте правильность написания названия предмета,\n',
            'предмет должнен быть написан с большой буквы\n',
            "например: 'Математика'\n",
            'Так же стоит проверить год и букву класса.'
        )

        return

    subject = Subject.objects.get(id=lesson.subject.id)
    teacher = Teacher.objects.get(id=lesson.teacher.id)

    commendations = [
        'Молодец!',
        'Отлично!',
        'Великолепно!',
        'Талантливо!',
        'Я тобой горжусь!',
        'Очень хороший ответ!',
        'Так держать!'
    ]

    Commendation.objects.create (
        text=choice(commendations),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=subject,
        teacher=teacher
    )

    print (
        'Похвала для ученика',
        '{schoolkid_full_name} на предмете {subject_name}'.format (
            schoolkid_full_name=schoolkid.full_name,
            subject_name=lesson.subject
        ),
        'от {lesson_date} успешно добавлена'.format (
            lesson_date=lesson.date
        )
    )