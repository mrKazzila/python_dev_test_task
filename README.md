<h1 align="center">
  <br>
  Code checker
  <br>
</h1>

<h4 align="center">
    Test task for python developer role at Skyeng
    <br>
</h4>

<div align="center">

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

</div>
<hr>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#tech-stack">Tech stack</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#additional-material">Additional material</a>
</p>


## Features
* Registration new user
* Authorisation
* Uploading python files
* Checking user uploaded python files with flake8, scheduled check via celery
* Sending an email message to the user about the results of checking the files he has uploaded
* Creating a report for the user based on the inspection


## Tech stack
- [Django](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Celery](https://docs.celeryq.dev/en/stable/index.html)
- [Bootstrap](https://getbootstrap.com/)


## How To Use
To clone and run this project, you'll need:
- [Git](https://git-scm.com)
- [Python](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)


<details>

<summary><strong>Use Docker</strong></summary>

1. Firstly clone repo
   ```bash
   git clone git@github.com:mrKazzila/python_dev_test_task.git
   ```

2. Prepare env with make
   ```bash
   make prepare_env
   ```

3. Run docker compose with make
   ```bash
   make docker_run
   ```

4. Stop docker compose with make
   ```bash
   make docker_stop
   ```

</details>

<details>

<summary>Other useful commands</summary>

1. Run tests
   ```bash
   make test
   ```

2. Run linters & formatters
   ```bash
   make test_linters
   ```

3. Reload docker
   ```bash
   make docker_reload
   ```

</details>



## Additional material
[test-assignment](readme/Тестовое%20задание%20на%20вакансию%20Python-разработчик.pdf)
