import os
from highcharts import Highchart
from .main import get_credits_by_job
from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello_world():
    stats = get_credits_by_job(os.environ.get("CIRCLE_TOKEN"), "gh/silvercar/mob-api")
    keys = [k for k, _ in stats.items()]
    values = [v for _, v in stats.items()]

    chart = Highchart()

    chart.set_options("chart", {"inverted": True})

    options = {
        "title": {"text": "Total Credits Used by CircleCI Workflow Job"},
        "xAxis": {
            "categories": keys,
            "title": {"text": None},
            "maxPadding": 0.05,
            "showLastLabel": True,
        },
        "yAxis": {
            "title": {"text": "Total Credits Used"},
            "labels": {
                "formatter": "function () {\
                    return this.value;\
                }"
            },
            "lineWidth": 2,
        },
        "legend": {"enabled": False},
        "tooltip": {
            "headerFormat": "<b>{series.name}</b><br/>",
            "pointFormat": "{point.x} : {point.y}",
        },
    }

    chart.set_dict_options(options)
    chart.add_data_set(values, "bar", "Total Credits Used")

    return str(chart)
