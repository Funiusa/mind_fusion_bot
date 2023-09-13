# Makefile
D = docker
DC = docker-compose
DC_RUN = docker-compose run --rm

up:
	$(DC) up

run_api:
	$(DC_RUN) -p 8000:8000 api $(ARGS)

run_bot:
	$(DC_RUN) bot $(ARGS)

upd:
	$(DC) up -d $(ARGS)

build:
	$(DC) build

clean:
	$(DC) down

prune:
	$(D) system prune -a && $(D) network prune && $(D) volume prune -a && $(D) builder prune -f

info:
	$(D) system df

re_api: clean build run_api

re_bot: clean build run_bot

fclean: clean prune

