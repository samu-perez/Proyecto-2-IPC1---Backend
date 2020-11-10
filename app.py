from flask import Flask, jsonify, request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from Usuario import Usuario
from Administrador import Administrador
from Cancion import Cancion
from Solicitud import Solicitud
from Comentario import Comentario
from Playlist import Playlist

#Declarando una lista
Usuarios = []
Administradores = []
Canciones = []
Solicitudes = []
contCanciones = 0 
contSolicitudes = 0
Comentarios = []
Playlists = []

Usuarios.append(Usuario('Samuel','Perez','samu', '123'))
Administradores.append(Administrador('Usuario', 'Maestro', 'admin', 'admin'))

@app.route('/ping')
def ping():
    return jsonify({'message': 'Ponggg!'})

@app.route('/usuarios', methods = ['GET'])
def obtenerUsuarios():
    global Usuarios
    Datos = []

    for usuario in Usuarios:
        #Formando el JSON, segun la estructura del JSON lo formamos como un objeto
        Dato = {
            'Nombre': usuario.getNombre(), 
            'Apellido': usuario.getApellido(), 
            'Username': usuario.getUsername(),
            'Contra': usuario.getContraseña()
            }
        Datos.append(Dato)

    respuesta = jsonify(Datos)
    return(respuesta)

@app.route('/usuarios/<string:username>', methods = ['GET'])
def obtenerUsuario(username):
    global Usuarios, Administradores
    comparador = False

    for usuario in Usuarios:
        if username == usuario.getUsername():
            Dato = {
               'Nombre': usuario.getNombre(),
               'Apellido': usuario.getApellido(),
               'Username': usuario.getUsername(),
               'Contra': usuario.getContraseña()
                }
            comparador = True
            break

    for admin in Administradores:
        if username == admin.getUsername():
            Dato = {
               'Nombre': admin.getNombre(),
               'Apellido': admin.getApellido(),
               'Username': admin.getUsername(),
               'Contra': admin.getContraseña()
                }
            comparador = True
            break

    if comparador == False:
        return jsonify({'message':'Usuario no agregado'})

    #No hace falta el else
    respuesta = jsonify(Dato)
    return(respuesta)

@app.route('/usuarios', methods = ['POST'])
def agregarUsuario():
    global Usuarios
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    username = request.json['username']
    contraseña = request.json['contraseña']
    encontrado = False
    
    for usuario in Usuarios:
        if usuario.getUsername() == username:
            encontrado = True
            break
    
    if encontrado == True:
        return jsonify({
            'message': 'Failed',
            'reason': 'El usuario ya fue registrado.'
            })
    else: 
        newUsuario = Usuario(nombre, apellido, username, contraseña)
        #Agregandolo a la Lista
        Usuarios.append(newUsuario)
        return jsonify({
            'message':'Success',
            'reason': 'Usuario agregado'
            })

@app.route('/usuarios/<string:username>', methods = ['PUT'])
def actualizarUsuario(username):
    global Usuarios

    for usuario in Usuarios:
        if username == usuario.getUsername():
            usuario.setNombre(request.json['nombre'])
            usuario.setApellido(request.json['apellido'])
            usuario.setUsername(request.json['username'])
            usuario.setContraseña(request.json['contraseña'])
            break

    return jsonify({'message':'Datos actualizados exitosamente'})

@app.route('/usuarios/<string:username>', methods = ['DELETE'])
def eliminarUsuario(username):
    global Usuarios

    for i in range(len(Usuarios)):
        if username == Usuarios[i].getUsername():
            del Usuarios[i]
            break

    return jsonify({'message': 'Usuario eliminado.'})

#-----------PARA ADMINS----------------
@app.route('/admins', methods = ['POST'])
def agregarAdmin():
    global Administradores
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    username = request.json['username']
    contraseña = request.json['contraseña']
    encontrado = False
    
    for admin in Administradores:
        if admin.getUsername() == username:
            encontrado = True
            break
    
    if encontrado == True:
        return jsonify({
            'message': 'Failed',
            'reason': 'El usuario ya fue registrado.'
            })
    else: 
        newAdmin = Administrador(nombre, apellido, username, contraseña)
        #Agregandolo a la Lista
        Administradores.append(newAdmin)
        return jsonify({
            'message':'Success',
            'reason': 'Usuario agregado'
            })

#--------------PARA INICIO DE SESION------------
@app.route('/login', methods = ['POST'])
def Login():
    global Usuarios, Administradores
    username = request.json['username']
    contraseña = request.json['contraseña']

    comparador = False

    for admin in Administradores:
        if username == admin.getUsername() and contraseña == admin.getContraseña():
            Dato = {
                'message': 'Success Admin',
                'usuario': admin.getUsername()
            }
            comparador = True
            break

    if(comparador == False):
        for usuario in Usuarios:
            if username == usuario.getUsername() and contraseña == usuario.getContraseña():
                Dato = {
                    'message': 'Success Cliente',
                    'usuario': usuario.getUsername()
                }
                break
            else:
                Dato = {
                    'message': 'Failed',
                    'usuario': ''
                }

    respuesta = jsonify(Dato)
    return(respuesta)

@app.route('/recuperarContra', methods = ['POST'])
def recuperarContra():
    global Usuarios
    username = request.json['username']

    for usuario in Usuarios:
        if username == usuario.getUsername():
            Dato = {
                'message': 'Success',
                'contraseña': usuario.getContraseña()
            }
            break
        else:
            Dato = {
                'message': 'Failed',
                'contraseña': ''
            }
    
    respuesta = jsonify(Dato)
    return(respuesta)

#-------PARA CANCIONES---------
@app.route('/canciones', methods = ['POST'])
def agregarCancion():
    global Canciones, contCanciones
    id = contCanciones
    nombre = request.json['nombre']
    artista = request.json['artista']
    album = request.json['album']
    imagen = request.json['imagen']
    fecha = request.json['fecha']
    spotify = request.json['spotify']
    youtube = request.json['youtube']

    newCancion = Cancion(id, nombre, artista, album, imagen, fecha, spotify, youtube)
    Canciones.append(newCancion)
    contCanciones += 1

    return jsonify({
        'message': 'Success',
        'reason': 'Cancion agregada'
    })

@app.route('/canciones', methods = ['GET'])
def obtenerCanciones():
    global Canciones
    Datos = []

    for cancion in Canciones:
        Dato = {
            'id': cancion.getId(),
            'nombre': cancion.getNombre(),
            'artista': cancion.getArtista(),
            'album': cancion.getAlbum(),
            'imagen': cancion.getImagen(),
            'fecha': cancion.getFecha(),
            'spotify': cancion.getSpotify(),
            'youtube': cancion.getYoutube()
        }
        Datos.append(Dato)
    
    respuesta = jsonify(Datos)
    return(respuesta)

@app.route('/canciones/<string:id>', methods = ['GET'])
def obtenerCancion(id):
    global Canciones
    comparador = False

    for cancion in Canciones:
        if int(id) == cancion.getId():
            Dato = {
               'nombre': cancion.getNombre(),
               'artista': cancion.getArtista(),
               'album': cancion.getAlbum(),
               'imagen': cancion.getImagen(),
               'fecha': cancion.getFecha(),
               'spotify': cancion.getSpotify(),
               'youtube': cancion.getYoutube()
                }
            comparador = True
            break

    if comparador == False:
        return jsonify({'message':'Cancion no agregada'})

    #No hace falta el else
    respuesta = jsonify(Dato)
    return(respuesta)

@app.route('/canciones/<string:id>', methods = ['PUT'])
def actualizarCancion(id):
    global Canciones

    for cancion in Canciones:
        if int(id) == cancion.getId():
            cancion.setNombre(request.json['nombre'])
            cancion.setArtista(request.json['artista'])
            cancion.setAlbum(request.json['album'])
            cancion.setImagen(request.json['imagen'])
            cancion.setFecha(request.json['fecha'])
            cancion.setSpotify(request.json['spotify'])
            cancion.setYoutube(request.json['youtube'])
            break

    return jsonify({'message':'Datos actualizados exitosamente'})

@app.route('/canciones/<string:id>', methods = ['DELETE'])
def eliminarCancion(id):
    global Canciones

    for i in range(len(Canciones)):
        if int(id) == Canciones[i].getId():
            del Canciones[i]
            break

    return jsonify({'message': 'Cancion eliminada.'})

#-------PARA SOLICITUDES---------
@app.route('/solicitudes', methods = ['POST'])
def agregarSolicitud():
    global Solicitudes, contSolicitudes
    id = contSolicitudes
    nombre = request.json['nombre']
    artista = request.json['artista']
    album = request.json['album']
    imagen = request.json['imagen']
    fecha = request.json['fecha']
    spotify = request.json['spotify']
    youtube = request.json['youtube']

    newSolicitud = Solicitud(id, nombre, artista, album, imagen, fecha, spotify, youtube)
    Solicitudes.append(newSolicitud)
    contSolicitudes += 1

    return jsonify({
        'message': 'Success',
        'reason': 'Solicitud enviada'
    })

@app.route('/solicitudes', methods = ['GET'])
def obtenerSolicitudes():
    global Solicitudes
    Datos = []

    for solicitud in Solicitudes:
        Dato = {
            'id': solicitud.getId(),
            'nombre': solicitud.getNombre(),
            'artista': solicitud.getArtista(),
            'album': solicitud.getAlbum(),
            'imagen': solicitud.getImagen(),
            'fecha': solicitud.getFecha(),
            'spotify': solicitud.getSpotify(),
            'youtube': solicitud.getYoutube()
        }
        Datos.append(Dato)
    
    respuesta = jsonify(Datos)
    return(respuesta)

@app.route('/solicitudes/<string:id>', methods = ['GET'])
def obtenerSolicitud(id):
    global Solicitudes
    comparador = False

    for solicitud in Solicitudes:
        if int(id) == solicitud.getId():
            Dato = {
               'nombre': solicitud.getNombre(),
               'artista': solicitud.getArtista(),
               'album': solicitud.getAlbum(),
               'imagen': solicitud.getImagen(),
               'fecha': solicitud.getFecha(),
               'spotify': solicitud.getSpotify(),
               'youtube': solicitud.getYoutube()
                }
            comparador = True
            break

    if comparador == False:
        return jsonify({'message':'Solicitud no agregada'})

    #No hace falta el else
    respuesta = jsonify(Dato)
    return(respuesta)

@app.route('/solicitudes/<string:id>', methods = ['DELETE'])
def rechazarSolicitud(id):
    global Solicitudes

    for i in range(len(Solicitudes)):
        if int(id) == Solicitudes[i].getId():
            del Solicitudes[i]
            break

    return jsonify({'message': 'Solicitud rechazada.'})

#-------PARA COMENTARIOS---------
@app.route('/comentarios', methods = ['POST'])
def agregarComentario():
    global Comentarios
    usuario = request.json['usuario']
    comentario = request.json['comentario']
    idCancion = request.json['idCancion']

    newComentario = Comentario(usuario, comentario, idCancion)
    Comentarios.append(newComentario)

    return jsonify({
        'message': 'Success',
        'reason': 'Comentario agregado'
    })

@app.route('/comentarios/<string:id>', methods = ['GET'])
def obtenerComentarios(id):
    global Comentarios
    Datos = []

    for comentario in Comentarios:
        if id == comentario.getIdCancion():
            Dato = {
                'usuario': comentario.getUsuario(),
                'comentario': comentario.getComentario(),
                'idCancion': comentario.getIdCancion()
            }
            Datos.append(Dato)
    
    respuesta = jsonify(Datos)
    return(respuesta)

#-------PARA PLAYLISTS---------
@app.route('/playlist', methods = ['POST'])
def agregarPlaylist():
    global Playlists
    usuario = request.json['usuario']
    spotify = request.json['spotify']

    newPlaylist = Playlist(usuario, spotify)
    Playlists.append(newPlaylist)

    return jsonify({
        'message': 'Success',
        'reason': 'Se agrego a mi Playlist'
    })

@app.route('/playlist/<string:usuario>', methods = ['GET'])
def obtenerPlaylist(usuario):
    global Playlists
    Datos = []

    for play in Playlists:
        if usuario == play.getUsuario():
            Dato = {
                'usuario': play.getUsuario(),
                'spotify': play.getSpotify()
            }
            Datos.append(Dato)
    
    respuesta = jsonify(Datos)
    return(respuesta)

if __name__ == '__main__':
    app.run(debug = True, port = 3000)