from krita import *
import json
from pathlib import Path
import sys
#import numpy as np
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import NamedTuple, Callable
from PyQt5.QtCore import QByteArray, QUrl, QFile, QBuffer
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import zlib
from multiprocessing import shared_memory

class Request(NamedTuple):
    url: str
    future: asyncio.Future
    buffer: QBuffer | None = None



class KritaComfyuiTransceiverExtension(Extension):

    def __init__(self, parent):
        # これは親クラスを初期化します。サブクラス化の際に重要です。
        self._net = QNetworkAccessManager()
        self._requests: dict[QNetworkReply, Request] = {}
        super().__init__(parent)

    def setup(self):
        pass

    def post(self, data: bytes):
        url = "http://localhost:8189/transceiver_post"
        request = QNetworkRequest(QUrl(url))
        request.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)
        data_bytes = QByteArray(data)
        reply = self._net.post(request, data_bytes)
        assert reply is not None, f"Network request for {url} failed: reply is None"
        return reply

    def start_transceiver(self):
        doc =  Krita.instance().activeDocument()
        if doc is None: return
        debug = dict()

        width = doc.width()
        height = doc.height()
        offset_nbytes = 2
        max_length = 2 ** (8 * offset_nbytes) - offset_nbytes

        layers = doc.topLevelNodes()
        for i, layer in enumerate(layers):
            if not layer.type() == 'paintlayer': continue
            
            literal_data_field = {
                "shape" : (height, width, 4),
                "dtype": "uint8",
                "name": layer.name()
            }
            serialized = repr(literal_data_field).encode("utf-8")
            assert len(serialized) <= max_length
            length_bytes = len(serialized).to_bytes(length=offset_nbytes, byteorder="big")
            layer_pixel_data = layer.projectionPixelData(0, 0, width, height).data()
            data = (
                length_bytes +
                serialized +
                layer_pixel_data
            )
            compressed = zlib.compress(data)
            self.post(b"ok"+compressed)
            break
#    }}}
            

    def stop_transceiver(self):
        pass

    def createActions(self, window):
        action = window.createAction("start_transceiver", "start transceiver")
        action.triggered.connect(self.start_transceiver)

#        action = window.createAction("stop_transceiver", "stop transceiver")
#        action.triggered.connect(self.stop_transceiver)



"""
    "activeNode",
    "animationLength",
    "annotation",
    "annotationDescription",
    "annotationTypes",
    "backgroundColor",
    "batchmode",
    "blockSignals",
    "bounds",
    "childEvent",
    "children",
    "clone",
    "close",
    "colorDepth",
    "colorModel",
    "colorProfile",
    "connectNotify",
    "createCloneLayer",
    "createColorizeMask",
    "createFileLayer",
    "createFillLayer",
    "createFilterLayer",
    "createFilterMask",
    "createGroupLayer",
    "createNode",
    "createSelectionMask",
    "createTransformMask",
    "createTransparencyMask",
    "createVectorLayer",
    "crop",
    "currentTime",
    "customEvent",
    "deleteLater",
    "destroyed",
    "disconnect",
    "disconnectNotify",
    "documentInfo",
    "dumpObjectInfo",
    "dumpObjectTree",
    "dynamicPropertyNames",
    "event",
    "eventFilter",
    "exportImage",
    "fileName",
    "findChild",
    "findChildren",
    "flatten",
    "framesPerSecond",
    "fullClipRangeEndTime",
    "fullClipRangeStartTime",
    "guidesLocked",
    "guidesVisible",
    "height",
    "horizontalGuides",
    "importAnimation",
    "inherits",
    "installEventFilter",
    "isSignalConnected",
    "isWidgetType",
    "isWindowType",
    "killTimer",
    "lock",
    "metaObject",
    "modified",
    "moveToThread",
    "name",
    "nodeByName",
    "nodeByUniqueID",
    "objectName",
    "objectNameChanged",
    "parent",
    "pixelData",
    "playBackEndTime",
    "playBackStartTime",
    "projection",
    "property",
    "pyqtConfigure",
    "receivers",
    "refreshProjection",
    "removeAnnotation",
    "removeEventFilter",
    "resizeImage",
    "resolution",
    "rootNode",
    "rotateImage",
    "save",
    "saveAs",
    "scaleImage",
    "selection",
    "sender",
    "senderSignalIndex",
    "setActiveNode",
    "setAnnotation",
    "setBackgroundColor",
    "setBatchmode",
    "setColorProfile",
    "setColorSpace",
    "setCurrentTime",
    "setDocumentInfo",
    "setFileName",
    "setFramesPerSecond",
    "setFullClipRangeEndTime",
    "setFullClipRangeStartTime",
    "setGuidesLocked",
    "setGuidesVisible",
    "setHeight",
    "setHorizontalGuides",
    "setModified",
    "setName",
    "setObjectName",
    "setParent",
    "setPlayBackRange",
    "setProperty",
    "setResolution",
    "setSelection",
    "setVerticalGuides",
    "setWidth",
    "setXOffset",
    "setXRes",
    "setYOffset",
    "setYRes",
    "shearImage",
    "signalsBlocked",
    "startTimer",
    "staticMetaObject",
    "thread",
    "thumbnail",
    "timerEvent",
    "topLevelNodes",
    "tr",
    "tryBarrierLock",
    "unlock",
    "verticalGuides",
    "waitForDone",
    "width",
    "xOffset",
    "xRes",
    "yOffset",
    "yRes"
"""
Krita.instance().addExtension(KritaComfyuiTransceiverExtension(Krita.instance()))