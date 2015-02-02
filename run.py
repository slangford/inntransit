#!/usr/bin/env python
from app import app
app.config.from_pyfile("aws.cfg")
app.run(debug = True)
