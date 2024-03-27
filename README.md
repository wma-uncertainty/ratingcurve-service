# ratingcurve-service

## Development Environment

Build the docker image locally

```bash
docker build -t ratingcurve-service --file Dockerfile .
```

### Test Docker Deployment

Test the deployment with

```bash
# FIXME
docker run -d -p 5000:4000 -e PORT=4000 ratingcurve-service

docker container list

docker logs <container-id>

# debug container
docker exec -it <container-id> bash

docker stop <container-id>
docker rm <container-id>
```

Might need to start docker daemon first.

```bash
sudo dockerd
```

### Test docker-compose Deployment

```bash
docker compose up --build
```

the `--build` argument makes Docker Compose build each image before instantiating containers

```bash
docker compose ps
```

```bash
docker compose down --volumes
```

#### Flask deployment

```bash
export FLASK_APP=rating_service
export FLASK_ENV=development
flask run --debug
```

or

```bash
flask --app rating_service run --debug
```
