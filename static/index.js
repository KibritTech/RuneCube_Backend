const sio = io();

sio.on('connect', () => {
  console.log('connected');
  sio.emit('check_rune', {rune_id:2}, (result) =>{
    console.log(result, "asdfghjklwertyuio");
});

sio.on('rune_check', (count) => {
    console.log(count.data);
})
});


sio.on('disconnect', () => {
  console.log('disconnected');
});

sio.on('choose_player', {user:'explorer'}, (ready) =>{
    console.log(ready);
});

