default:
	@echo targets: gunicorn 
	@echo targets: venv
	@echo targets: build
	@echo targets: bash
	@echo targets: runDocker

gunicorn:
	gunicorn -w 4 webapp3:server

venv:
	@echo source ~/github/slexil/py3105/bin/activate

build:
	docker build -t pshannon/slexil1 .

bash:
	docker run \
      -v /Users/paul/github/slexil/docker/TEXTS:/app/texts \
      -v /Users/paul/github/slexil/docker/PROJECTS:/app/PROJECTS \
      -ti --rm -p 9004:80 pshannon/slexil1 bash


runDocker:
	docker run \
      -v /Users/paul/github/slexil/docker/TEXTS:/app/texts \
      -v /Users/paul/github/slexil/docker/PROJECTS:/app/PROJECTS \
      -ti --rm -p 9005:80 pshannon/slexil1

