# Petition Hackathon Project

## Docker build

1. Install Docker and docker-compose.
   
For Debian, Ubuntu:

```
su
apt update; apt upgrade -y; apt install -y curl; curl -sSL https://get.docker.com/ | sh; curl -L https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose
```

Don't forget press CTRL+D to exit from super user account.

2. Build docker images:

```
docker-compose build
```
cp example.env .env
```

3. Run docker-compose:

```
docker-compose up
```

4. Enjoy!