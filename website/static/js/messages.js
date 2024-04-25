document.addEventListener('DOMContentLoaded', function() {
    const closeBtn = document.querySelector('.close-btn');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            const notificationContainer = document.querySelector('.notification-container');
            if (notificationContainer) {
                notificationContainer.style.display = 'none';
            }
        });
    }
});
