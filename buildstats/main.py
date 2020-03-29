import requests
import os
from requests.utils import default_user_agent
import pprint


def main():
    pprint.pprint(get_jobs(os.environ.get("CIRCLE_TOKEN"), "gh/silvercar/mob-api"))
    stats = get_credits_by_job(os.environ.get("CIRCLE_TOKEN"), "gh/silvercar/mob-api")
    print("\n".join("{:<24}\t{:>10}".format(k, v) for k, v in stats.items()))
    print("\n")
    stats = get_duration_by_job(os.environ.get("CIRCLE_TOKEN"), "gh/silvercar/mob-api")
    print("\n".join("{:<24}\t{:>10}".format(k, v) for k, v in stats.items()))


def get_duration_by_job(circle_token, project_slug):
    jobs = get_jobs(circle_token, project_slug)

    return {
        job["name"]: job["metrics"]["duration_metrics"]["p95"]
        for job in sorted(
            jobs["items"],
            key=lambda job: job["metrics"]["duration_metrics"]["p95"],
            reverse=True,
        )
    }


def get_credits_by_job(circle_token, project_slug):
    jobs = get_jobs(circle_token, project_slug)

    return {
        job["name"]: job["metrics"]["total_credits_used"]
        for job in sorted(
            jobs["items"],
            key=lambda job: job["metrics"]["total_credits_used"],
            reverse=True,
        )
    }


def get_jobs(circle_token, project_slug):
    r = requests.get(
        "https://circleci.com/api/v2/insights/{0}/workflows/build/jobs".format(
            project_slug
        ),
        headers={
            "Circle-Token": circle_token,
            "User-Agent": "{0} {1}".format("tmhall99/buildstats", default_user_agent()),
        },
    )
    r.raise_for_status()
    jobs = r.json()

    if jobs["next_page_token"] is not None:
        print("Too many jobs")
        return

    return jobs


if __name__ == "__main__":
    main()
