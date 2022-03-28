const sio = io();

sio.on('connect', () => {
  console.log('connected');
  sio.emit('choose_player', {"username": "leila", "role": "saver"}, (start_game) =>{
    console.log(start_game, "checking leila");
});
sio.emit('choose_player', {"username": "nermin", "role": "explorer"}, (start_game) =>{
    console.log(start_game, "asdfghjklwertyuio");
});

sio.emit('start_game', (game) => {
    console.log(game, 'qqqqqqqqqqq');
})
});


sio.on('disconnect', () => {
  console.log('disconnected');
});

sio.on('choose_player', {"username": "leila", "role": "solver"}, (ready) =>{
    console.log(ready);
});

// sio.emit('check_rune', {"value": "cycle", "color": "red"}, (count) => {
//     console.log(count, 'cccccccccccccccc');
// })

