import sys

import typer
from rich.console import Console

from ikuai_api.api import *
from ikuai_api.utils import *

router: Router
console = Console()

app = typer.Typer()


@app.callback()
def init_router(
        username: str = typer.Option(None, help="用户名"),
        password: str = typer.Option(None, help="密码"),
        ip: str = typer.Option(None, help="ip"),
        port: int = typer.Option(80, help="端口")):
    if "--help" in sys.argv:
        return

    if not all([username, password, ip, port]):
        raise typer.BadParameter("必须提供 --username, --password 和 --ip")

    global router
    router = Router(username, password, ip, port)


@app.command()
def query_ssl():
    r = router.call('show', 'key_manager', {})
    console.print(r)


@app.command()
def update_ssl(publicKey: str = typer.Option(..., help="public key"),
               privateKey: str = typer.Option(..., help="private key"),
               enable: bool = typer.Option(..., help="是否启用")):
    publicKey = ssl_read(publicKey)
    privateKey = ssl_read(privateKey)

    return router.call('save', 'key_manager', {
        'ca': encode_ssl(publicKey),
        'comment': '',
        'enabled': 'yes' if enable else 'no',
        'id': 1,
        'key': encode_ssl(privateKey)
    })
