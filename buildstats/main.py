import requests
import os


def main():
    stats = getstats(os.environ.get("CIRCLE_TOKEN"))
    print(stats["text"])
    print(
        "\n".join(
            "{:<24}\t{:>10}".format(k, v) for k, v in stats["credits_used"].items()
        )
    )


def getstats(circle_token):
    result = dict()
    r = requests.get(
        "https://circleci.com/api/v2/insights/gh/silvercar/mob-api/workflows/build/jobs",
        headers={"Circle-Token": circle_token},
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
