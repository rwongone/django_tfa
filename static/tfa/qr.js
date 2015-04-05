$(document).ready(function() {
    new QRCode("qrcode", {
        text: tfaUri,
        width: 256,
        height: 256,
        colorDark : "#000000",
        colorLight : "#ffffff",
        correctLevel : QRCode.CorrectLevel.H
    });
});