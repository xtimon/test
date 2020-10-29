# Tech task

## Usage

```bash
ansible-galaxy install -r requirements.yml
vagrant up
```

## How to connect to vms

```bash
vagrant ssh machine1
vagrant ssh machine2
vagrant ssh machine3
```

## How to access metrics

Prometheus is avaiable on url [http://localhost:9090](http://localhost:9090)

Grafana is avaiable on url [http://localhost:3000](http://localhost:3000)

Grafana default credentials:

```yaml
user: admin
password: changeme
```

## How to cleanup resources

```bash
vagrant destroy -f
```

## Requirements

- Virtualbox
- Vagrant
- Ansible
