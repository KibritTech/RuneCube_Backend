const sio = io();

sio.on('connect', () => {
  console.log('connected');
  sio.emit('choose_player', {"username": "leila", "role": "saver"}, (ready) =>{
    console.log(ready, "asdfghjklwertyuio");
});
sio.emit('choose_player', {"username": "leila", "role": "explorer"}, (ready) =>{
    console.log(ready, "asdfghjklwertyuio");
});

sio.on('rune_check', (count) => {
    console.log(count.data);
})
});


sio.on('disconnect', () => {
  console.log('disconnected');
});

sio.on('choose_player', {"username": "leila", "role": "solver"}, (ready) =>{
    console.log(ready);
});

