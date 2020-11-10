class Administrador:

    def __init__(self, nombre, apellido, username, contraseña):
        self.nombre = nombre
        self.apellido = apellido
        self.username = username
        self.contraseña = contraseña
    
    #Metodos get
    def getNombre(self):
        return self.nombre
    
    def getApellido(self):
        return self.apellido
    
    def getUsername(self):
        return self.username

    def getContraseña(self):
        return self.contraseña

    #Metodos set
    def setNombre(self, nombre):
        self.nombre = nombre

    def setApellido(self, apellido):
        self.apellido = apellido

    def setUsername(self, username):
        self.username = username
    
    def setContraseña(self, contraseña):
        self.contraseña = contraseña