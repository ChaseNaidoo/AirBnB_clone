#!/usr/bin/python3
"""Package Initialization"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
