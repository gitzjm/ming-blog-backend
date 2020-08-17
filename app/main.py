# coding=UTF-8

"""``main``
"""

import uvicorn

from core.conf import conf

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=conf.server.host,
        port=int(conf.server.port),
        log_level="info",
        debug=bool(conf.server.debug)
    )
