from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike
from random import sample, randint

class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio for data generation')

    def handle(self, *args, **options):
        ratio = options['ratio']
        
        # Очистка старых данных
        QuestionLike.objects.all().delete()
        AnswerLike.objects.all().delete()
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Tag.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        # Создаем пользователей
        users = []
        for i in range(ratio):
            user = User.objects.create_user(
                username=f'user_{i}',
                email=f'user_{i}@example.com',
                password='password123'
            )
            profile = Profile.objects.create(user=user)
            users.append(user)
            if i % 100 == 0:
                self.stdout.write(f'Created {i} users...')

        # Создаем теги
        tags = []
        for i in range(ratio):
            tag = Tag.objects.create(name=f'tag_{i}')
            tags.append(tag)
            if i % 100 == 0:
                self.stdout.write(f'Created {i} tags...')

        # Создаем вопросы
        questions = []
        for i in range(ratio * 10):
            author = users[randint(0, len(users)-1)]
            question = Question.objects.create(
                title=f'Question {i}',
                text=f'This is text for question {i}',
                author=author
            )
            # Добавляем 1-3 случайных тега к вопросу
            question.tags.set(sample(tags, k=randint(1, 3)))
            questions.append(question)
            if i % 1000 == 0:
                self.stdout.write(f'Created {i} questions...')

        # Создаем ответы
        answers = []
        for i in range(ratio * 100):
            author = users[randint(0, len(users)-1)]
            question = questions[randint(0, len(questions)-1)]
            answer = Answer.objects.create(
                text=f'This is answer {i} to question {question.id}',
                author=author,
                question=question
            )
            answers.append(answer)
            if i % 10000 == 0:
                self.stdout.write(f'Created {i} answers...')

        # Создаем лайки с проверкой уникальности
        like_count = 0
        for i in range(ratio * 200):
            user = users[randint(0, len(users)-1)]
            if i % 2 == 0:
                # Лайк вопроса
                question = questions[randint(0, len(questions)-1)]
                _, created = QuestionLike.objects.get_or_create(
                    user=user,
                    question=question
                )
                if created:
                    like_count += 1
            else:
                # Лайк ответа
                answer = answers[randint(0, len(answers)-1)]
                _, created = AnswerLike.objects.get_or_create(
                    user=user,
                    answer=answer
                )
                if created:
                    like_count += 1
            if i % 10000 == 0:
                self.stdout.write(f'Created {like_count} likes...')

        self.stdout.write(self.style.SUCCESS(
            f'Successfully filled database. Stats:\n'
            f'Users: {len(users)}\n'
            f'Tags: {len(tags)}\n'
            f'Questions: {len(questions)}\n'
            f'Answers: {len(answers)}\n'
            f'Likes: {like_count}'
        ))