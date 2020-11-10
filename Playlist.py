class Playlist:
    def __init__(self, usuario, spotify):
        self.usuario = usuario
        self.spotify = spotify

    #Metodos get
    def getUsuario(self):
        return self.usuario

    def getSpotify(self):
        return self.spotify

    #Metodos set
    def setUsuario(self, usuario):
        self.usuario = usuario

    def setSpotify(self, spotify):
        self.spotify = spotify