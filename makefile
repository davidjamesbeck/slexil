default:
	@targets: gunicorn 
	@targets: venv
	@targets: build
	@targets: bash
	@targets: runDocker

gunicorn:
	gunicorn -w 4 webapp3:server

venv:
	@echo source ~/github/slexil/py3105/bin/activate

build:
	docker build -t pshannon/slexil1 .

bash:
	docker run \
       -v /Users/paul/github/slexil/docker/PROJECTS:/app/PROJECTS \
       -ti --rm -p 9004:80 pshannon/slexil1 bash


runDocker:
	docker run \
      -v /Users/paul/github/slexil/docker/PROJECTS:/app/PROJECTS \
      -ti --rm -p 9005:80 pshannon/slexil1

