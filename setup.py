from setuptools import setup, find_packages



version = open("VERSION").read().strip()
PROJECT_DESC = "Tool for injecting attacks into serial data bus datasets"
PROJECT_URL = "https://github.com/matthewRekos/serialNightshade"
PACKAGE_NAME = "nightshade"

setup(
    name="serialNightshade-test",
    version=version,
    description=PROJECT_DESC,
    long_description=open("README.md").read(),
    #long_description_content_type="text/markdown",
    url=PROJECT_URL,
    author="matthewRekos",
    author_email="redacted_for_submission",
    # packages=[PACKAGE_NAME, "{}.tests".format(PACKAGE_NAME), "{}.utils".format(PACKAGE_NAME)],
    # Add any non-python package files to this list to be captured in pypi packaging
    # package_data={PACKAGE_NAME: ["data/*", "data/configs/*"]},
    # install_requires=INSTALL_REQUIRES,
    entry_points={
        "console_scripts": [
            "nightshade = serialNightshade.main:begin_attacks"
        ],
    },
    data_files=[(".", ["VERSION"])],
    # package_dir={"":"."},
    packages=find_packages(where="."),
)
