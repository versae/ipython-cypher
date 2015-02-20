# -*- coding: utf-8 -*-
from neo4jrestclient.client import GraphDatabase

from cypher.utils import urlparse


class Connection(object):
    current = None
    connections = {}

    @classmethod
    def tell_format(cls):
        return (
            "Format: (http|https)://username:password@hostname:port/db/name, "
            "or one of %s"
        ) % str(cls.connections.keys())

    def __init__(self, connect_str=None, alias=None):
        try:
            if connect_str in self.connections:
                gdb = GraphDatabase(self.connections[connect_str])
            else:
                gdb = GraphDatabase(connect_str)
                alias = connect_str
        except:
            print(self.tell_format())
            raise
        self.name = alias or self.assign_name(gdb)
        self.session = gdb
        self.connections[self.name] = self
        self.connections[gdb.url] = self
        Connection.current = self

    @classmethod
    def get(cls, descriptor):
        if isinstance(descriptor, Connection):
            cls.current = descriptor
        elif descriptor:
            conn = (cls.connections.get(descriptor) or
                    cls.connections.get(descriptor.lower()))
            if conn:
                cls.current = conn
            else:
                cls.current = Connection(descriptor)
        if cls.current:
            return cls.current
        else:
            raise Exception(cls.tell_format())

    @classmethod
    def assign_name(cls, gdb):
        splits = urlparse(gdb.url)
        core_name = '%s@%s' % (gdb._auth['username'], splits.hostname)
        incrementer = 1
        name = core_name
        while name in cls.connections:
            name = '%s_%d' % (core_name, incrementer)
            incrementer += 1
        return name
