class BgpHandler():
    counter=0
    def __init__(self,pkt):
        self.pkt=pkt

    def convert_to_ascii(self):
         return "".join(str(ord(char)) for char in self.pkt)

    def check_update(self):
        y=self.convert_to_ascii()
        if ((y[:48]=="255255255255255255255255255255255255255255255255") and (int(y[51])==2) and y[52:56]=="0000"):
            return (True,y[56:])
        return (False,"")

    def get_uri(self):
        a=self.check_update()
        if (a[0]==True):
            return a[1]
        return "No bgp"
