import socketio

sio = socketio.Server()
main = socketio.WSGIApp(sio, static_files={
    '/':'./static/'
})

explorer = 0
solver = 0
ready = False


class Rune:
    def __init__(self, count, time):
        self.count = count
        self.time = time





@sio.event
def connect(sid, environ):
    pass


@sio.event
def disconnect(sid):
    pass


#sid is session id, it is assigned to client when it connects, 
#environ is a dict that has all the details from client request like if they have any errors or cookies in environ
@sio.event
def choose_player(sid, data):
    global explorer
    global solver
    global ready
    print(sid, "id is over here")
    print(data, "data is over here")
    print(type(data['user']), "data user is over here")
    print(explorer)
    if data['user'] == 'explorer' and  explorer == 0:
        explorer += 1
        print(explorer, 'explorer count +1 ')

    # if data['user'] == 'solver' and  solver == 0:
    #     solver += 1

    elif data['user'] == 'explorer' and  explorer != 0:
        sio.emit('choose_player', {'data': 'Role is already taken'})

    # elif data['user'] == 'solver' and  solver != 0:
    #     sio.emit('choose_player', {'data': 'Role is already taken'})
    
    if explorer == 1 and solver == 1:
        ready = True
        return ready



@sio.event
def started_game(sid):
    sio.emit('rune_data', Rune, to=sid)

        


   


