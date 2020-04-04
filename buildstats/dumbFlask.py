import os
from highcharts import Highchart
from .main import get_credits_by_job, get_duration_by_job
from flask import Flask


app = Flask(__name__)


@app.route("/credits")
def credits():
    return renderChart(
        get_credits_by_job(os.environ.get("CIRCLE_TOKEN"), "gh/silvercar/mob-api"),
        "Total Credits Used",
    )


@app.route("/duration")
def duration():
    return renderChart(
        get_duration_by_job(os.environ.get("CIRCLE_TOKEN"), "gh/silvercar/mob-api"),
        "Duration",
    )


def renderChart(stats, bottom, left="Workflow Job"):
    keys = [k for k, _ in stats.items()]
    values = [v for _, v in stats.items()]

    chart = Highchart()

    chart.set_options("chart", {"inverted": True})

    options = {
        "title": {"text": "{0} by {1}".format(bottom, left)},
        "xAxis": {
            "categories": keys,
            "title": {"text": left},
            "maxPadding": 0.05,
            "showLastLabel": True,
        },
        "yAxis": {
            "title": {"text": bottom},
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
    chart.add_data_set(values, "bar")

    return str(chart)
