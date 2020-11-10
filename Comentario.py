class Comentario:
    def __init__(self, usuario, comentario, idCancion):
        self.usuario = usuario
        self.comentario = comentario
        self.idCancion = idCancion

    #Metodos get
    def getUsuario(self):
        return self.usuario

    def getComentario(self):
        return self.comentario

    def getIdCancion(self):
        return self.idCancion

    #Metodos set
    def setUsuario(self, usuario):
        self.usuario = usuario

    def setComentario(self, comentario):
        self.comentario = comentario

    def setIdCancion(self, idCancion):
        self.idCancion = idCancion