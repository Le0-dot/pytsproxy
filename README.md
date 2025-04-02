# pytsproxy

Small python web server to use as discover target for tailscale devices in prometheus.

## Installation

### Docker

```sh
docker pull ghcr.io/le0-dot/pytsproxy:latest
```

### Host

```sh
git clone https://github.com/Le0-dot/pytsproxy.git
cd pytsproxy
python -m venv .venv
source .venv/bin/activate
pip install .
```

## Usage

### To see help

```sh
pytsproxy -h
```

### To run on port 8080
```sh
docker run ghcr.io/le0-dot/pytsproxy
```

Or

```sh
pytsproxy -p 8080
```

## Plugging in

To use this web server in prometheus use should put the following URL

```
http://{SERVER}:{PORT}/{TAILNET}/{TAG}
```

TAILNET is the organization name of your tailnet, see [tailscale admin console](https://login.tailscale.com/admin/settings/general).
TAG is the device tag on which the machines will be filtered.

Additionally, `Authorization` header should be sent to the proxy with tailscale API key, see [tailscale API docs](https://tailscale.com/api#description/authentication).
