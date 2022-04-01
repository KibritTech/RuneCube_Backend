const sio = io();

sio.on('connect', () => {
  console.log('connected');
//   sio.emit('choose_player', {"username": "leila", "role": "saver"}, (start_game) =>{
//     console.log(start_game, "checking leila");
// });
// sio.emit('choose_player', {"username": "nermin", "role": "explorer"}, (start_game) =>{
//     console.log(start_game, "asdfghjklwertyuio");
// });

// sio.emit('start_game', (game) => {
//     console.log(game, 'qqqqqqqqqqq');
// })
});


sio.on('disconnect', () => {
//   console.log('disconnected', reason);
//   sio.emit('reconnect', {"username": "ekber"}, (ready) => {
//       console.log(ready, "reconnect")
//   })
});

// sio.emit('finish_time', (result) => {
//     console.log(result, 'finis time...........')
//   });

// sio.on('choose_player', {"username": "leila", "role": "solver"}, (ready) =>{
//     console.log(ready);
// });

sio.emit('check_rune', {"value": "Circle", "color": "Yellow"}, (count) => {
    console.log(count, 'cccccccccccccccc');
});

    