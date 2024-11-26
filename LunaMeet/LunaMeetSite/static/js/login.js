const form = document.getElementById('form');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(form);

    try {
        const response = await fetch('http://127.0.0.1:8000/user-sign-in', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            window.location.href = 'http://127.0.0.1:8000';
            sessionStorage.setItem('authToken', result.token);
        } else {
            showPopup(result.error, false);
        }
    } catch (error) {
        console.log(error);
        // Покажем всплывающее окно при сетевой ошибке
        showPopup('Ошибка сети. Попробуйте снова позже.', false);
    }
});

// Функция для отображения всплывающего окна
function showPopup(message, isSuccess) {
    const popup = document.createElement('div');
    popup.className = 'popup';
    popup.textContent = message;

    if (isSuccess) {
        popup.classList.add('success');
    } else {
        popup.classList.add('error');
    }

    document.body.appendChild(popup);

    // Закрыть окно через 3 секунды
    setTimeout(() => {
        popup.remove();
    }, 3000);
}
