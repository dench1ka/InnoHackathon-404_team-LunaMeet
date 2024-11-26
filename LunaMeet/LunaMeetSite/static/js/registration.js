const form = document.getElementById("form")

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(form);

    try {
        const response = await fetch('http://127.0.0.1:8000/user-sign-up', {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            showPopup(result.message, true);
        } else {
            showPopup(result.error, false)
        }
    } catch (error) {
        console.log(error)
    }
})


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