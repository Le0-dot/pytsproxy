import json
from argparse import ArgumentParser
from collections.abc import Iterable
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
from typing import Any, NotRequired, TypedDict
from urllib.request import Request, urlopen


class Device(TypedDict):
    addresses: list[str]
    id: str
    nodeId: str
    user: str
    name: str
    hostname: str
    clientVersion: str
    updateAvailable: bool
    os: str
    created: str
    lastSeen: str
    keyExpiryDisabled: bool
    expires: str
    authorized: bool
    isExternal: bool
    machineKey: str
    nodeKey: str
    blocksIncomingConnections: bool
    enabledRoutes: list[str]
    advertisedRoutes: list[str]
    clientConnectivity: dict[str, Any]
    tags: NotRequired[list[str]]
    tailnetLockError: str
    tailnetLockKey: str
    postureIdentity: dict[str, Any]


def tailscale_devices(tailnet: str, tag: str, token: str) -> Iterable[str]:
    request = Request(
        f"https://api.tailscale.com/api/v2/tailnet/{tailnet}/devices",
        headers={"Authorization": token},
    )

    with urlopen(request) as response:
        devices: list[Device] = json.load(response)["devices"]

    tagged = filter(lambda device: f"tag:{tag}" in device.get("tags", []), devices)
    return map(lambda device: device["name"], tagged)


class TailscaleAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path_parts = list(filter(bool, self.path.split("/")))

        try:
            tailnet, tag = path_parts
        except ValueError:
            self.send_response(HTTPStatus.NOT_FOUND)
            return

        if (bearer_token := self.headers["Authorization"]) is None:
            self.send_response(HTTPStatus.UNAUTHORIZED)
            return

        names = tailscale_devices(tailnet, tag, bearer_token)
        response_data = [{"targets": list(names)}]

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/json")
        self.end_headers()

        response = json.dumps(response_data)
        _ = self.wfile.write(response.encode())


def main() -> None:
    parser = ArgumentParser()
    _ = parser.add_argument(
        "-p",
        "--port",
        type=int,
        required=True,
        choices=range(1, 2**16),
        metavar="[1-65535]",
        help="Port number on which server will run.",
    )

    args = parser.parse_args()

    with TCPServer(("", args.port), TailscaleAPIHandler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    main()
