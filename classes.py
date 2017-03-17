class ObjectNetwork():
    def __init__(self, name):
        self.name = name
        self.children = []

class ObjectGroupNetwork():
    def __init__(self, name):
        self.name = name
        self.children = []

class ObjectGroupService():
    def __init__(self, name):
        self.name = name
        self.children = []

class Line():
    def __init__(self):
        self.acl = None
        self.protocol = None
        self.action = None
        self.remark = None
        self.source = None
        self.destination = None
        self.service = None
