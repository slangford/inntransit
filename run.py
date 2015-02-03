#!/usr/bin/env python
from app import app
app.config.from_pyfile("aws.cfg")
app.run('0.0.0.0', port=5000)
