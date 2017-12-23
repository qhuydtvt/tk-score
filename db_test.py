from models.score import Score
from mlab import mlab_connect

mlab_connect()

db_scores = Score.objects()
for db_score in db_scores:
    print(db_score.name, db_score.score)