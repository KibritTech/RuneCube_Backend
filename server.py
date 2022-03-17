import socketio

sio = socketio.Server()
main = socketio.WSGIApp(sio, static_files={
    '/':'./static/'
})






class Rune:
    # rune_id = 2
    def __init__(self,rune_id=1, rune_count=5, max_response_time=12, each_side_count=60, sides_count = 6):
        """
        :param rune_count: how many runes will be in each side
        :param max_response_time: The time given to a player to answer a question
        :param each_side_count: The time between each cube side  ( seconds )
        :param sides_count: How many sides will have a rune (it is fixed )
        :return:
        """
        self.rune_id = rune_id
        self.rune_count = rune_count
        self.max_response_time = max_response_time
        self.each_side_count = each_side_count
        self.sides_count = sides_count

    def showData(self):
      print(self.rune_count)

a = Rune()
print(a.rune_id)


class Player:
    def __init__(self, sid, username):
        self.sid = sid
        self.username = username


@sio.event
def connect(sid, environ):
    print(f"client with {sid} connected")
    
    # print(f"'environ' {environ}")




@sio.event
def disconnect(sid):
    
    print(f"client with {sid} disconnected")


#sid is session id, it is assigned to client when it connects, 
#environ is a dict that has all the details from client request like if they have any errors or cookies in environ
@sio.event
def choose_player(sid, data):
    explorer = 0
    solver = 0
    ready = False
    # global explorer
    # global solver
    # global ready
    print(sid, "id is over here")
    print(data, "data is over here")
    print(type(data['user']), "data user is over here")
    print(explorer)
    if data['user'] == 'explorer' and  explorer == 0:
        explorer += 1
        print(explorer, 'explorer count +1 ')

    if data['user'] == 'solver' and  solver == 0:
        solver += 1

    # elif data['user'] == 'explorer' and  explorer != 0:
    #     sio.emit('choose_player', {'data': 'Role is already taken'})

    # elif data['user'] == 'solver' and  solver != 0:
    #     sio.emit('choose_player', {'data': 'Role is already taken'})
    
    if explorer == 1 and solver == 1:
        ready = True
        return ready


@sio.event
def started_game(sid):
    return Rune


@sio.event
def check_rune(sid, data):
    rune_id = data['rune_id']
    global rune_count
    cc = Rune()
    print(cc.rune_count)
    rune_count = cc.rune_count
    if rune_id == cc.rune_id:
        if rune_count > 0:
            rune_count -= 1
            print(rune_count, 'rune count123')
            sio.emit('rune_check', rune_count)
        sio.emit('rune_check', {'data': 'Rune side finished'})
    sio.emit('rune_check',  {'data': 'Ne tot Rune'})
        

    

        


   


