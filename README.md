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
  <a href="https://mrkazzila.github.io/python_dev_test_task/">GitHub Pages</a> •
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

<summary><strong>Local run use Docker</strong></summary>

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

<summary>Other useful local commands</summary>

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


<details>

<summary>Base deploy command</summary>

0. Prepare you server
 - Updating local packages: `sudo apt-get update && apt-get upgrade -y`
 - Recommended: Create a new user `adduser <username>` & `usermod -aG sudo <username>`
 - Recommended: Copy SSH-key to server
 - Recommended: Update sshd_config
 - [Install docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
 - Install make `sudo apt-get install make`
 - [Setup UFW](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-18-04-ru)

1. Prepare env with make
   ```bash
   make prepare_env
   ```
2. Update the information in the .env files

3. Run docker compose prod with make
   ```bash
   make docker_prod_run
   ```
4. Enter to django container
   ```bash
   make django_container_enter
   ```

- Other useful prod commands

1. Clean all
   ```bash
   make docker_remove_all_force
   ```

</details>



## Additional material
[test-assignment](readme/Тестовое%20задание%20на%20вакансию%20Python-разработчик.pdf)
