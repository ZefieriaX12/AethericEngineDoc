from datetime import timezone, timedelta, datetime

class SocketMsg:
    order: int
    data: bytes
    dt: datetime

    def __init__(self, order:int, data:bytes, dt:datetime):
        self.order = order
        self.dt = dt
        self.data = data

    def hasData(self):
        if (self.data != None) & (len(self.data) > 0):
            return True
        return False
    
    def isEmpty(self):
        if (self.data == None) | (len(self.data) == 0):
            return True
        return False
    
