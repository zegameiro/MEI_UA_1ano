# Docker 101

## Vagrant Installation

We will install `docker-io` from the original repositories.
We also set the Memory used by Virtualbox to 1GB and create a Host Only Network.
This network will allow direct communication between the host and the guest.

Consider the `Vagrantfile` in this folder. It will create a virtual machine with docker and some configuration to access the DETI
Docker registry.

After creating the machine, you can enter it with `vagrant ssh` and you can access services exposed using the Internal Network IP Address.
By default it is `192.168.56.10`

Keep all work in the synchronized folder `/vagrant` so that you can edit files in the host.

If you do not wish to run a virtual machine, and prefer your own system, execute the provisioning script of the `Vagrantfile` as a super user.
It was tested on Ubuntu Jammy but should work on other Ubuntu distributions. 

__Windows__

Follow the steps into this [link](https://docs.docker.com/desktop/windows/wsl/).

__MacOS__

Follow the steps into this [link](https://docs.docker.com/desktop/install/mac-install/).
Take care to select the correct CPU type (M1 and M2 are arm based).

In both cases, edit the file `/etc/docker/daemon.json` and add:
```json
{
  "default-address-pools" : [
    {
      "base" : "10.139.0.0/16",
      "size" : 24
    }
  ]
}
```

Then restart the docker daemon.


## Validation

In the host with docker (Virtual Machine or host), run:

```bash
docker run hello-world
docker run -it ubuntu bash
```

## Examples

### App

```bash
docker build --network=host -t registry.deti/prof/app:v1 .
docker push registry.deti/prof/app:v1
docker run -p 8080:8080 registry.deti/prof/app:v1
```

### App persistence

```bash
docker build --network=host -t registry.deti/prof/app-persistence:v1 .
docker push registry.deti/prof/app-persistence:v1
docker run -p 8080:8080 --mount type=bind,source="$(pwd)"/www,target=/app/www registry.deti/prof/app-persistence:v1
```

### App compose

```bash
docker compose up
```

### App Swarm

Skip due to lack of access

### App config

```bash
docker compose up
```

### App secrets

```bash
docker compose up
```

## Cheat Sheet

Remove all the unused images, volumes and networks

```
docker system prune --all
```

## References

1. [Dockerfile](https://docs.docker.com/engine/reference/builder/)
2. [The Ultimate Docker Cheat Sheet](https://dockerlabs.collabnix.com/docker/cheatsheet/)
3. [Docker Commands Cheat Sheet](https://pagertree.com/blog/docker-commands-cheat-sheet)