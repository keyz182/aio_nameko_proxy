# coding=utf-8
import logging
from aio_nameko_proxy import AIOClusterRpcProxy
from aio_nameko_proxy.pool import PoolItemContextManager


class _Cluster(object):

    def __init__(self, ctx: "ContextVar"):
        self.ctx = ctx
        self.token = None
        self.obj = None

    def _set(self, obj):
        self.obj = obj
        if self.token is not None:
            self.ctx.reset(self.token)
        self.token = self.ctx.set(obj)

    def __getattr__(self, name):
        instance = self.ctx.get(None)
        if not instance:
            # raise RuntimeError("Please initialize your cluster before using")
            instance = self.obj
        return getattr(instance, name)


class _ForHint:
    async def get_proxy(self):
        pass

    def remove(self) -> None:
        pass

    def release_proxy(self, proxy: "AIOClusterRpcProxy") -> None:
        pass

    def acquire(self) -> PoolItemContextManager:
        pass


from typing import cast

rpc_cluster = cast(_ForHint, _Cluster())

from .sanic import SanicNamekoClusterRpcProxy
from .fastapi import FastApiNamekoProxyMiddleware
