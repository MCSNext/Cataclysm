clientapi=None
serverapi=None


def set_clientApi(cls):
    global clientapi
    clientapi=cls

def set_serverapi(cls):
    global serverapi
    serverapi=cls