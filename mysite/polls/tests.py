from django.test import TestCase
from .models import Question, Choice
from django.utils import timezone
from django.test import Client
import json

# Create your tests here.


def add(x, y):
    return x + y


def sub(x, y):
    return y - x


class CalculatorTest(TestCase):
    def test_add(self):
        result = add(1, 3)
        self.assertEquals(result, 4)

    def test_sub(self):
        result = sub(2, 3)
        self.assertEquals(result, 0)


class QuestionAPITest(TestCase):
    def setUp(self):
        now = timezone.now()
        questions = [
            {
                "question_text": 'who are you',
                'pub_date': now,
                'is_published': False
            },
            {
                "question_text": 'what is the time',
                'pub_date': now,
                'is_published': False
            },
            {
                "question_text": 'where are you going',
                'pub_date': now,
                'is_published': True
            }
        ]
        for q_dict in questions:
            q = Question.objects.create(**q_dict)
            for i in range(3):
                Choice.objects.create(
                        question=q,
                        choice_text="choice-" + str(i),
                        votes=0
                    )
    def test_question_api(self):
        print("Setup is successful")
        client = Client()
        response = client.get("/polls/api/question")
        self.assertEqual(response.status_code,200)
        json_content = json.loads(response.content.decode('utf-8'))
        items = json_content['items']
        for item in items:
            q = Question.objects.get(pk=item['id'])
            self.assertEqual(q.question_text, item['question_text'])

        self.assertEqual(Question.objects.count(),len(item))
