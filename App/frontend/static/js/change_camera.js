// camera stream video element
let videoElm = document.querySelector('#video');
// flip button element
let flipBtn = document.querySelector('#flip-btn');

// default user media options
let defaultsOpts = { audio: false, video: true }
let shouldFaceUser = false;

// check whether we can use facingMode
let supports = navigator.mediaDevices.getSupportedConstraints();
if( supports['facingMode'] === true ) {
  flipBtn.disabled = false;
}

let stream = null;

function capture() {
  defaultsOpts.video = { facingMode: shouldFaceUser ? 'user' : 'environment' }
  navigator.mediaDevices.getUserMedia(defaultsOpts)
    .then(function(_stream) {
      stream  = _stream;
      videoElm.srcObject = stream;
      videoElm.play();
    })
    .catch(function(err) {
      console.log(err)
    });
}

flipBtn.addEventListener('click', function(){
  if( stream == null ) return
  // we need to flip, stop everything
  stream.getTracks().forEach(t => {
    t.stop();
  });
  // toggle / flip
  shouldFaceUser = !shouldFaceUser;
  capture();
})

capture();