#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
from typing import Any

import uvicorn

from src.core import ApplicationSettings
from src.services.utils.other.api_installation import (
    Director,
    DevelopmentApplicationBuilderLoggedProxy,
)


def run_application(**kwargs: Any) -> None:
    """
    !NOT FOR PRODUCTION! \n
    Function, which start an application \n
    Instead of it use gunicorn with uvicorn workers. e.g. \n
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

    :return: None, just run application with uvicorn
    """
    settings = ApplicationSettings()
    director = Director(DevelopmentApplicationBuilderLoggedProxy(settings=settings))
    app = director.configure()
    uvicorn.run(app, **kwargs)  # type: ignore  # noqa


if __name__ == "__main__":
    run_application()
    # subprocess.run(["gunicorn", "-w 4", "-k uvicorn.workers.UvicornWorker", "main:app"])
