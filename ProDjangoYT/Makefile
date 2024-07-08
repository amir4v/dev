Makefile

make is a tool used in compiling software and it's a linux tool.

This file is going to be made up of something called targets and aunder your target you have your recipe.

prereqs (Prerequisites) are kind of like triggers that when the prerequisites change it can cause the recipe to be re-run.

target:
	recipe

run-server:
	poetry run python manage.py runserver

make run-server

target: target anotherTarget ;

Whenever you create a make file by default it assumes that these targets are actual files, so we should say they are just custom commands that we built and we should do that with .PHONY keyword:
	.PHONY: targetName
	targetName:
		command...

.PHONY: install-pre-commit
install-pre-commit: # each line will be run in a separate shell
	poetry run pre-commit uninstall
	poetry run pre-commit install

.PHONY: install-pre-commit
install-pre-commit: # in on shell
	poetry run pre-commit uninstall; poetry run pre-commit install

.PHONY: up-dependencies-only
up-dependencies-only:
	test -f .env || touch .env
	docker-compose -f docker-compose.dev.yaml up --force-recreate db

.PHONY: test
test:
	poetry test -v -rs -n auto --show-capture=no
	# -v -> Verbose the output and describe more.
	# -rs -> show me a summery of skip tests at the end (r=report, s=skipped) -> report those skipped ones.
	# -n auto -> run these tests across as many cores as we have.
	# --show-capture=no -> don't show the apps outputs.
