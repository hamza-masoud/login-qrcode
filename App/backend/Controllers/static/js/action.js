(function () {
    const video = document.getElementById('video'),
        canvas = document.getElementById('canvas'),
        context = canvas.getContext('2d'),
        photo = document.getElementById('photo'),
        vendorUrl = window.URL || webkitURL;

    navigator.getMedia = navigator.getUserMedia ||
        navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia ||
        navigator.msGetUserMedia;

    navigator.getUserMedia({
        video: true,
        audio: false
    }, function (stream) {
        video.srcObject = stream;
        video.play();
    }, function (error) {
        // an error
        // error.code
    });

    document.getElementById('capture').addEventListener('click', function () {
        context.drawImage(video, 0, 0, 400, 300);
        photo.setAttribute('src', canvas.toDataURL('image/png'));

    });
})();
document.getElementById('capture').addEventListener('click', function () {
    var canvas = document.getElementById('canvas');
    var dataURL = canvas.toDataURL();
    var textinput = document.getElementById('text-input');
    textinput.setAttribute('value', dataURL);
    document.getElementById("form").submit();
});