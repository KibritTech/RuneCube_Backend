const sio = io();

sio.on('connect', () => {
  console.log('connected');
  sio.emit('choose_player', {"username": "leila", "role": "saver"}, (start_game) =>{
    console.log(start_game, "checking leile");
});
sio.emit('choose_player', {"username": "nermin", "role": "explorer"}, (start_game) =>{
    console.log(start_game, "asdfghjklwertyuio");
});

sio.on('rune_check', (count) => {
    console.log(count.data);
})

sio.emit('start_game', {"username": "leila", "role": "saver"}, (game) => {
    console.log(game.data);
})

});


sio.on('disconnect', () => {
  console.log('disconnected');
});

sio.on('choose_player', {"username": "leila", "role": "solver"}, (ready) =>{
    console.log(ready);
});

