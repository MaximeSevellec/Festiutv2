document.addEventListener('DOMContentLoaded', function () {
    var flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(function (message) {
        var timeout = 3000;  // 4 secondes

        setTimeout(function () {
            message.style.opacity = 0;
            setTimeout(function () {
                message.remove();
            }, 500);
        }, timeout);
    });
});