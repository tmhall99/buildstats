import requests
import os
from requests.utils import default_user_agent


def main():
    stats = get_credits_used(os.environ.get("CIRCLE_TOKEN"), "gh/silvercar/mob-api")
    print(stats["text"])
    print(
        "\n".join(
            "{:<24}\t{:>10}".format(k, v) for k, v in stats["credits_used"].items()
        )
    )


def get_credits_used(circle_token, project_slug):
    result = dict()
    r = requests.get(
        "https://circleci.com/api/v2/insights/{0}/workflows/build/jobs".format(
            project_slug
        ),
        headers={
            "Circle-Token": circle_token,
            "User-Agent": "{0} {1}".format("tmhall99/buildstats", default_user_agent()),
        },
    )
    result["text"] = r.text
    jobs = r.json()

    if jobs["next_page_token"] is not None:
        print("Too many jobs")
        return

    result["credits_used"] = {
        job["name"]: job["metrics"]["total_credits_used"]
        for job in sorted(
            jobs["items"],
            key=lambda job: job["metrics"]["total_credits_used"],
            reverse=True,
        )
    }
    return result


if __name__ == "__main__":
    main()
