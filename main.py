import rollbar
import sys
import git

# usage:
# from rollbar_logger import rollbar_init, rollbar_except_hook
# rollbar_init('YOUR_ENVIRONMENT')
# sys.excepthook = rollbar_except_hook

ROLLBAR_POST_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"


# optional for code_version
def get_git_sha():
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.commit.hexsha
    short_sha = repo.git.rev_parse(sha, short=4)
    print(f'Git short sha: {short_sha}')
    return short_sha


def rollbar_init(environment):
    rollbar.init(
        access_token=ROLLBAR_POST_ACCESS_TOKEN,
        environment=environment,
        code_version=get_git_sha(), # optional
    )
    rollbar.report_message(f'Rollbar is configured correctly for {environment}')

# custom except_hook method
def rollbar_except_hook(exc_type, exc_value, traceback):
    # Report the issue to rollbar here.
    rollbar.report_exc_info((exc_type, exc_value, traceback))
    # display the error as normal here
    sys.__excepthook__(exc_type, exc_value, traceback)


def proof_of_concept():
    rollbar_init('poc-test')
    # override sys.excepthook with the custom except_hook method
    sys.excepthook = rollbar_except_hook

    a = 'c'
    b = 1
    c = a + b

if __name__ == '__main__':
    proof_of_concept()