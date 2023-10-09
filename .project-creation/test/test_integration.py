import os

from pytest_check import check


@check.check_func
def is_dir(path: str):
    assert os.path.isdir(path)


@check.check_func
def is_file(path: str):
    assert os.path.isfile(path)


def test_files_in_place():
    os.chdir(os.environ["VELOCITAS_APP_ROOT"])

    # devcontainer
    is_dir(".devcontainer")
    is_dir(".devcontainer/scripts")
    is_file(".devcontainer/scripts/configure-proxies.sh")
    is_file(".devcontainer/scripts/container-set.sh")
    is_file(".devcontainer/scripts/onCreateCommand.sh")
    is_file(".devcontainer/scripts/postStartCommand.sh")
    is_file(".devcontainer/devcontainer.json")
    is_file(".devcontainer/Dockerfile")

    # github integration
    is_dir(".github")
    is_dir(".github/actions")
    is_dir(".github/actions/pre-commit-action")
    is_file(".github/actions/pre-commit-action/action.yml")
    is_dir(".github/ISSUE_TEMPLATE")
    is_file(".github/ISSUE_TEMPLATE/bug-report.yml")
    is_file(".github/ISSUE_TEMPLATE/feature-request.yml")
    is_file(".github/ISSUE_TEMPLATE/question.yml")

    is_dir(".github/scripts")
    is_file(".github/scripts/deploy_image_from_artifact.sh")
    is_file(".github/scripts/junit.tpl")

    is_dir(".github/workflows")
    is_file(".github/workflows/build-docker-image.yml")
    is_file(".github/workflows/build-multiarch-image.yml")
    is_file(".github/workflows/check-licenses.yml")
    is_file(".github/workflows/ci.yml")
    is_file(".github/workflows/ensure-lifecycle.yml")
    is_file(".github/workflows/gen-desired-state.yml")
    is_file(".github/workflows/release.yml")
    is_file(".github/dependabot.yml")
    is_file(".github/PULL_REQUEST_TEMPLATE.yml")

    # vscode project
    is_dir(".vscode")
    is_file(".vscode/launch.json")
    is_file(".vscode/settings.json")
    is_file(".vscode/tasks.json")

    # app
    is_dir("app")
    is_file("app/src/main.py")
    is_dir("app/tests")
    is_file("app/AppManifest.json")
    is_file("app/Dockerfile")
    is_file("app/requirements-velocitas.txt")
    is_file("app/requirements.in")
    is_file("app/requirements.txt")

    # general things
    is_file(".editorconfig")
    is_file(".gitattributes")
    is_file(".gitignore")
    is_file(".licensechecker.yml")
    is_file(".pre-commit-config.yaml")
    is_file(".velocitas.json")
    is_file("LICENSE")
    is_file("license_header.txt")
    is_file("NOTICE-3RD-PARTY-CONTENT.md")
    is_file("NOTICE.md")
    is_file("README.md")
    is_file("requirements.in")
    is_file("requirements.txt")
    is_file("setup.cfg")
    is_file("whitelisted-licenses.txt")
