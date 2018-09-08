from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    is_published = models.BooleanField(default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "question_text": self.question_text,
            "choice": [c.to_dict() for c in self.choice_set.all()]
        }

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "choice_text": self.choice_text,
            "votes": self.votes
        }

    def __str__(self):
        return "{}:{}".format(self.question.question_text, self.choice_text)
