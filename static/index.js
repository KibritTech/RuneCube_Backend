const sio = io();

sio.on('connect', () => {
  console.log('connected');
  sio.emit('choose_player', {user:'explorer'}, (ready) =>{
      console.log(ready);
  });
});


sio.on('disconnect', () => {
  console.log('disconnected');
});

// sio.on('sum_result', (data) =>{
//     console.log(data);
// })

// sio.on('mult', (data, cb) => {
//     const result = data.numbers[0] * data.numbers[1];
//     cb(result);
//     // console.log(result);
// })