class Ampel(object):
    def __init__(self):
        self.rot = False
        self.gelb = False
        self.gruen = False
        
class Ampelsteuerung(object):
    
    def ausschalten(self, ampel):
        ampel.rot = False
        ampel.gelb = False
        ampel.gruen = False

    def anschalten(self, ampel, farbe):        
        if farbe == "rot":
            ampel.rot = True
        if farbe == "gelb":
            ampel.gelb = True
        if farbe == "gruen":
            ampel.gruen = True
    
    def aufGruen(self, ampel):        
        self.ausschalten(ampel)
        self.anschalten(ampel, "gelb")
        self.ausschalten(ampel)
        self.anschalten(ampel, "gruen")
        
    def aufRot(self, ampel):
        self.ausschalten(ampel)
        self.anschalten(ampel, "gelb")
        self.ausschalten(ampel)
        self.anschalten(ampel, "rot")
    
    def status(self, ampel):
        return [ampel.rot, ampel.gelb, ampel.gruen]
