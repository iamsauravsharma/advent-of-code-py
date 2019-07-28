import appdirs
import os
from pathlib import Path
from .server_action import download_input
import time


def check_if_downloaded(year, day, session):
    """
    Check if really a input is downloaded or not and cached
    """
    cache_file = join_path(year, day, session, input=True)
    cache_file = Path(cache_file)
    return cache_file.exists()


def save_input_to_location(year, day, session, input):
    """
    Save a input to its location
    """
    cache_folder = join_path(year, day, session)
    Path(cache_folder).mkdir(parents=True, exist_ok=True)
    cache_file = os.path.join(cache_folder, "input.txt")
    with open(cache_file, "w+") as f:
        f.write(input)


def delete_input(year, day, session):
    """
    Delete input from a cache folders
    """
    cache_file = join_path(year, day, session, input=True)
    if Path(cache_file).exists():
        os.remove(cache_file)


def cache_file_data(year, day, session):
    """
    Return cache file data from cache
    """
    download_input(year, day, session)
    cache_file = join_path(year, day, session, input=True)
    with open(cache_file) as f:
        input_data = f.read()
    return input_data


def save_submitted_answer(year, day, part, session, output, message):
    """
    Save submitted input to  file
    """
    submitted_file = join_path(year, day, session, submission=True)
    with open(submitted_file, "a") as f:
        f.write("{}!{}:{}\n".format(part, output, message))


def check_if_answer_is_present(year, day, part, session, output):
    """
    Check is answer is already submitted
    """
    submission_file = join_path(year, day, session, submission=True)
    with open(submission_file, "r") as f:
        lines = f.read()
        for line in lines:
            seprate_part = line.split("!", 1)
            if seprate_part[0] == part:
                seprate_output = seprate_part[1].split(":", 1)
                if seprate_output == output:
                    raise Exception(
                        "You have already submitted this solution you got {}".format(
                            seprate_output[1]
                        )
                    )


def save_last_submission_time(year, day, session):
    """
    Save a time where a request is performed
    """
    last_time_file = join_path(year, day, session, last_file=True)
    with open(last_time_file, "w") as f:
        f.write(str(time.time()))


def check_last_submission_time(year, day, session):
    """
    Check last submission date raise error if time is less than 60 second
    """
    last_time_file = join_path(year, day, session, last_file=True)
    with open(last_time_file, "r") as f:
        last_time = float(f.read())
        current_time = time.time()
        if current_time - last_time < 60.0:
            raise Exception(
                "You have last submitted within 60 seconds for this solution"
            )


def join_path(year, day, session, input=False, submission=False, last_file=False):
    cache_location = appdirs.user_cache_dir()
    cache_file = os.path.join(cache_location, str(session), str(year), str(day))
    if input:
        cache_file = os.path.join(cache_file, "input.txt")
    if submission:
        cache_file = os.path.join(cache_file, "submission.txt")
    if last_file:
        cache_file = os.path.join(cache_file, "time.txt")
    return cache_file
