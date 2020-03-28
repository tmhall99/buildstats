import requests
import os


def main():
    r = requests.get(
        "https://circleci.com/api/v2/insights/gh/silvercar/mob-api/workflows/build/jobs",
        headers={"Circle-Token": os.environ.get("CIRCLE_TOKEN")},
    )
    print(r.text)
    jobs = r.json()

    if jobs["next_page_token"] is not None:
        print("Too many jobs")
        return

    s = {
        job["name"]: job["metrics"]["total_credits_used"]
        for job in sorted(
            jobs["items"],
            key=lambda job: job["metrics"]["total_credits_used"],
            reverse=True,
        )
    }
    print(s)


if __name__ == "__main__":
    main()
