import typer
from rich.console import Console

from ikuai_api.api import *
from ikuai_api.utils import *

console = Console()

app = typer.Typer()


@app.command()
def query_ssl(
        username: str = typer.Option(None, help="用户名", envvar='ROUTER_USERNAME'),
        password: str = typer.Option(None, help="密码", envvar='ROUTER_PASSWORD', hide_input=True, prompt="Password"),
        ip: str = typer.Option(None, help="ip", envvar='ROUTER_IP'),
        port: int = typer.Option(80, help="端口")):
    router = Router(username, password, ip, port)
    r = router.call('show', 'key_manager', {})
    console.print(r)


@app.command()
def update_ssl(username: str = typer.Option(..., help="用户名", envvar='ROUTER_USERNAME'),
               password: str = typer.Option(..., help="密码", envvar='ROUTER_PASSWORD', hide_input=True,
                                            prompt="Password"),
               ip: str = typer.Option(..., help="ip", envvar='ROUTER_IP'),
               port: int = typer.Option(80, help="端口"),

               publicKey: str = typer.Option(..., help="public key"),
               privateKey: str = typer.Option(..., help="private key"),
               enable: bool = typer.Option(..., help="是否启用")):
    router = Router(username, password, ip, port)

    publicKey = ssl_read(publicKey)
    privateKey = ssl_read(privateKey)

    r = router.call('save', 'key_manager', {
        'ca': encode_ssl(publicKey),
        'comment': '',
        'enabled': 'yes' if enable else 'no',
        'id': 1,
        'key': encode_ssl(privateKey)
    })
    console.print("证书更新成功")
