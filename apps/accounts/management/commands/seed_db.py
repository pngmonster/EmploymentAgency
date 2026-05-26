"""
Команда для заполнения БД тестовыми данными.
Запуск: python manage.py seed_db
"""
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction


APPLICANT_DATA = [
    ('Иванов',    'Алексей',    'Петрович',   'male',   'Moscow'),
    ('Смирнова',  'Мария',      'Игоревна',   'female', 'Saint Petersburg'),
    ('Козлов',    'Дмитрий',    'Андреевич',  'male',   'Novosibirsk'),
    ('Новикова',  'Анна',       'Сергеевна',  'female', 'Ekaterinburg'),
    ('Морозов',   'Сергей',     'Владимирович','male',  'Kazan'),
    ('Волкова',   'Елена',      'Николаевна', 'female', 'Nizhny Novgorod'),
    ('Лебедев',   'Артём',      'Дмитриевич', 'male',   'Samara'),
    ('Соколова',  'Ольга',      'Александровна','female','Omsk'),
    ('Зайцев',    'Николай',    'Михайлович', 'male',   'Rostov-on-Don'),
    ('Павлова',   'Татьяна',    'Юрьевна',    'female', 'Ufa'),
]

RESUME_TITLES = [
    'Python-разработчик', 'Frontend-разработчик', 'UI/UX Дизайнер',
    'Менеджер по продажам', 'Бухгалтер', 'Маркетолог',
    'DevOps-инженер', 'Аналитик данных', 'Проект-менеджер',
    'Системный администратор',
]

EMPLOYER_DATA = [
    ('Яндекс',       'IT',             2000, 'Moscow'),
    ('Сбербанк',     'Финансы',        1841, 'Moscow'),
    ('Тинькофф',     'Финансы',        2006, 'Moscow'),
    ('Ozon',         'E-commerce',     1998, 'Moscow'),
    ('2ГИС',         'IT',             1999, 'Novosibirsk'),
    ('Авито',        'IT',             2007, 'Moscow'),
    ('Wildberries',  'E-commerce',     2004, 'Moscow'),
    ('Газпром нефть','Энергетика',     1995, 'Saint Petersburg'),
    ('Ростелеком',   'Телекоммуникации',1993,'Moscow'),
    ('Мегафон',      'Телекоммуникации',1993,'Moscow'),
]

VACANCY_DATA = [
    ('Python Backend разработчик',  150000, 250000, 'remote',  3),
    ('Frontend React разработчик',  120000, 200000, 'hybrid',  2),
    ('DevOps Engineer',             180000, 300000, 'office',  4),
    ('Product Manager',             130000, 220000, 'hybrid',  3),
    ('UI/UX Designer',              100000, 170000, 'remote',  2),
    ('Data Analyst',                110000, 190000, 'office',  2),
    ('Менеджер по продажам',         60000, 120000, 'office',  1),
    ('Бухгалтер',                    70000, 100000, 'office',  3),
    ('Маркетолог',                   80000, 140000, 'hybrid',  2),
    ('Системный администратор',      90000, 150000, 'office',  3),
    ('Тестировщик QA',               90000, 160000, 'remote',  2),
    ('Аналитик данных Senior',      200000, 350000, 'remote',  5),
]

COVER_LETTERS = [
    'Здравствуйте! Меня очень заинтересовала ваша вакансия. Имею релевантный опыт и готов приступить к работе в ближайшее время.',
    'Добрый день! Считаю себя отличным кандидатом на эту позицию. Готов пройти собеседование в удобное для вас время.',
    'Уважаемые коллеги! Ваша компания давно привлекает моё внимание. Буду рад стать частью вашей команды.',
    'Здравствуйте! Обладаю необходимыми навыками и опытом для успешного выполнения задач на данной позиции.',
    'Добрый день! Ознакомился с описанием вакансии и уверен, что смогу принести пользу вашей компании.',
]


class Command(BaseCommand):
    help = 'Заполняет БД тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить данные перед заполнением',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        from apps.accounts.models import User
        from apps.applicants.models import Applicant, Resume
        from apps.employers.models import Employer
        from apps.vacancies.models import Vacancy, Application
        from apps.payments.models import Payment

        if options['clear']:
            self.stdout.write('🗑️  Очищаем тестовые данные...')
            User.objects.filter(email__endswith='@test.jobbureau.ru').delete()
            self.stdout.write(self.style.SUCCESS('Очищено.'))

        self.stdout.write('🌱 Заполняем БД тестовыми данными...\n')

        # ── Соискатели ───────────────────────────────────────
        self.stdout.write('👤 Создаём соискателей...')
        applicants = []
        for i, (last, first, middle, gender, city) in enumerate(APPLICANT_DATA):
            email = f'applicant{i+1}@test.jobbureau.ru'
            if User.objects.filter(email=email).exists():
                self.stdout.write(f'   Пропускаем {email} — уже существует')
                continue

            user = User.objects.create_user(
                email=email,
                password='testpass123',
                role='applicant',
            )
            user.is_verified = True
            user.save()

            applicant = Applicant.objects.create(
                user=user,
                last_name=last,
                first_name=first,
                middle_name=middle,
                gender=gender,
                phone=f'+7916{random.randint(1000000, 9999999)}',
                city=city,
                country='Россия',
                about=f'Опытный специалист с многолетним стажем. Готов к новым вызовам и интересным проектам.',
                status=random.choice(['actively_looking', 'open_to_offers']),
            )
            applicants.append(applicant)

            # Резюме
            for j in range(random.randint(1, 2)):
                Resume.objects.create(
                    applicant=applicant,
                    title=random.choice(RESUME_TITLES),
                    experience_years=random.randint(0, 10),
                    salary_expected=Decimal(random.choice([80000, 100000, 120000, 150000, 200000])),
                    education=random.choice(['bachelor', 'master', 'vocational']),
                    skills='Python, Django, PostgreSQL, Docker, Git',
                    status='active',
                )

        self.stdout.write(self.style.SUCCESS(f'   Создано {len(applicants)} соискателей'))

        # ── Работодатели ─────────────────────────────────────
        self.stdout.write('🏢 Создаём работодателей...')
        employers = []
        for i, (name, industry, year, city) in enumerate(EMPLOYER_DATA):
            email = f'employer{i+1}@test.jobbureau.ru'
            if User.objects.filter(email=email).exists():
                self.stdout.write(f'   Пропускаем {email} — уже существует')
                continue

            user = User.objects.create_user(
                email=email,
                password='testpass123',
                role='employer',
            )
            user.is_verified = True
            user.save()

            employer = Employer.objects.create(
                user=user,
                company_name=name,
                industry=industry,
                founded_year=year,
                city=city,
                country='Россия',
                about=f'{name} — ведущая компания в сфере {industry}. Мы ищем талантливых специалистов.',
                is_verified=random.choice([True, True, False]),
                contact_person='HR-отдел',
                phone=f'+7495{random.randint(1000000, 9999999)}',
                website=f'https://www.{name.lower().replace(" ", "")}.ru',
            )
            employers.append(employer)

        self.stdout.write(self.style.SUCCESS(f'   Создано {len(employers)} работодателей'))

        # ── Вакансии ─────────────────────────────────────────
        self.stdout.write('💼 Создаём вакансии...')
        vacancies = []
        all_employers = list(Employer.objects.all())

        for title, sal_min, sal_max, work_format, exp in VACANCY_DATA:
            if not all_employers:
                break
            employer = random.choice(all_employers)
            vacancy = Vacancy.objects.create(
                employer=employer,
                title=title,
                about=f'Мы ищем опытного специалиста на позицию {title}. '
                      f'Вы будете работать в дружной команде профессионалов. '
                      f'Предлагаем конкурентную зарплату и отличные условия труда.',
                experience_years=exp,
                salary_min=Decimal(sal_min),
                salary_max=Decimal(sal_max),
                employment_type='full_time',
                schedule=random.choice(['five_days', 'flexible']),
                work_format=work_format,
                city=employer.city,
                country='Россия',
                contact_name='HR-менеджер',
                contact_email=employer.user.email,
                status='active',
            )
            vacancies.append(vacancy)

        self.stdout.write(self.style.SUCCESS(f'   Создано {len(vacancies)} вакансий'))

        # ── Отклики ───────────────────────────────────────────
        self.stdout.write('📬 Создаём отклики...')
        app_count = 0
        all_resumes = list(Resume.objects.filter(status='active'))
        all_vacancies = list(Vacancy.objects.filter(status='active'))

        used_pairs = set()
        statuses = ['pending', 'pending', 'viewed', 'accepted', 'rejected']

        for resume in all_resumes:
            for vacancy in random.sample(all_vacancies, min(3, len(all_vacancies))):
                pair = (vacancy.id, resume.id)
                if pair in used_pairs:
                    continue
                used_pairs.add(pair)

                status = random.choice(statuses)
                fee = None
                if status == 'accepted':
                    avg = (vacancy.salary_min + vacancy.salary_max) / 2
                    fee = (avg * Decimal('0.001')).quantize(Decimal('0.01'))

                Application.objects.create(
                    vacancy=vacancy,
                    resume=resume,
                    cover_letter=random.choice(COVER_LETTERS),
                    status=status,
                    employer_comment='Спасибо за отклик!' if status == 'accepted' else (
                        'К сожалению, ваш опыт не соответствует требованиям.' if status == 'rejected' else ''
                    ),
                    fee=fee,
                    is_paid=False,
                )
                app_count += 1

        self.stdout.write(self.style.SUCCESS(f'   Создано {app_count} откликов'))

        # ── Платежи ───────────────────────────────────────────
        self.stdout.write('💳 Создаём платежи...')
        pay_count = 0
        for employer in random.sample(all_employers, min(5, len(all_employers))):
            if random.random() > 0.5:
                amount = Decimal(random.randint(5000, 50000))
                Payment.objects.create(
                    employer=employer,
                    amount=amount,
                    status='paid',
                    applications_snapshot=[],
                )
                pay_count += 1

        self.stdout.write(self.style.SUCCESS(f'   Создано {pay_count} платежей'))

        # ── Итог ──────────────────────────────────────────────
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ База данных заполнена тестовыми данными!'))
        self.stdout.write('')
        self.stdout.write('📋 Тестовые аккаунты (пароль для всех: testpass123):')
        self.stdout.write('   Соискатели: applicant1@test.jobbureau.ru ... applicant10@test.jobbureau.ru')
        self.stdout.write('   Работодатели: employer1@test.jobbureau.ru ... employer10@test.jobbureau.ru')
