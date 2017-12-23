from mlab import mlab_connect
from models.score import Score
from datetime import datetime, timedelta
from random import randint

mlab_connect()

for i in range(10):
    score = Score()
    score.name = "past"
    score.score = 120
    score.added_time = datetime.now() - timedelta(days=randint(1, 5))
    score.save()