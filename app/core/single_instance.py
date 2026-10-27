"""Only one Akeso at a time per Windows user.

The first Akeso listens on a local pipe. A second one connects to it, hands
over what it was started with (an akeso://join/... invite link, or just
"show"), and exits; the first one then comes to the front.

A crashed Akeso leaves no lock behind: if nobody answers on the pipe, the
newcomer clears the stale name and becomes the first.
"""

import getpass
import re

from PySide6.QtCore import QObject, Signal
from PySide6.QtNetwork import QLocalServer, QLocalSocket

CONNECT_MS = 600


def _name() -> str:
    user = re.sub(r"[^A-Za-z0-9_]", "_", getpass.getuser() or "user")
    return f"akeso-single-instance-{user}"


class SingleInstance(QObject):
    message = Signal(str)            # what a later start passed along ("show" or a link)

    def __init__(self) -> None:
        super().__init__()
        self._server = None

    def claim(self, payload: str = "show") -> bool:
        """True when this is the only Akeso. False when another one is already
        running: it has been told (payload) and this one should exit."""
        socket = QLocalSocket()
        socket.connectToServer(_name())
        if socket.waitForConnected(CONNECT_MS):
            socket.write((payload or "show").encode("utf-8"))
            socket.flush()
            socket.waitForBytesWritten(CONNECT_MS)
            socket.disconnectFromServer()
            return False
        QLocalServer.removeServer(_name())          # a leftover from a crash
        self._server = QLocalServer(self)
        self._server.setSocketOptions(QLocalServer.SocketOption.UserAccessOption)
        if not self._server.listen(_name()):
            self._server = None                     # can't listen: don't block starting
            return True
        self._server.newConnection.connect(self._accept)
        return True

    def _accept(self) -> None:
        while self._server is not None and self._server.hasPendingConnections():
            socket = self._server.nextPendingConnection()
            socket.readyRead.connect(lambda s=socket: self._read(s))
            socket.disconnected.connect(socket.deleteLater)
            if socket.bytesAvailable():
                self._read(socket)

    def _read(self, socket: QLocalSocket) -> None:
        text = bytes(socket.readAll()).decode("utf-8", errors="replace").strip()
        if text:
            self.message.emit(text[:2000])
