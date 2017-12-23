# 1 Import flask, flask-restful
from flask import Flask, request
from flask_restful import Api, Resource
from datetime import datetime, timedelta

from models.score import Score

from mlab import mlab_connect

# 2 Create flask app
app = Flask(__name__)
api = Api(app)
mlab_connect()

# 3 Create home route
@app.route("/")
def index():
    return "Hello world"

def criteria(json_score):
    return -json_score["score"]

# Create Score resource
class ScoreRes(Resource):
    def get(self):
        # 1. Get all scores from database
        db_scores = Score.objects()

        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow_start = today_start + timedelta(days=1)

        # 2. Convert all scores into json
        score_list = [
            {
                'name': db_score.name,
                'score': db_score.score
            }
            for db_score in db_scores
            if today_start <= db_score.added_time < tomorrow_start
        ]

        sorted_score_list = sorted(score_list, key=criteria)

        if len(sorted_score_list) > 10:
            return sorted_score_list[0: 10]
        else:
            return sorted_score_list

    def post(self):
        # 1. Get data from json body
        json_score = request.get_json()
        name = json_score["name"] # dictionary
        score = json_score["score"]
        added_time = datetime.now()

        # 2. Add name, score into database
        new_score = Score()
        new_score.name = name
        new_score.score = score
        new_score.added_time = added_time
        new_score.save()

        return {
            'success': 1,
            'data': {
                'name': new_score.name,
                'score': new_score.score
            }
        }


class TopScoreRes(Resource):
    def get(self):
        # 1. Get ALL scores
        db_scores = Score.objects()

        # 2. Get highest score
        score_list = [
            {
                'name': db_score.name,
                'score': db_score.score
            }
            for db_score in db_scores
        ]

        sorted_score_list = sorted(score_list, key=criteria)

        if len(sorted_score_list) > 0:

            highest_score = sorted_score_list[0]

            return {
                'success': 1,
                'data': highest_score
            }

        else:
            return {
                'success': 0,
                'message': 'No scores'
            }

# Add resource into API
api.add_resource(ScoreRes, "/score")
api.add_resource(TopScoreRes, "/top")


# 4 Run app
if __name__ == "__main__":
    app.run(debug=True, port=1212)