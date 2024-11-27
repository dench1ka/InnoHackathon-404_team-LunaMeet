document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const parts = window.location.href.split("/");
        const event_id = parts[parts.length - 1];
        formData.append('event_id', event_id);
        formData.append('token', sessionStorage.getItem('authToken'));

        try{
            const response = await fetch("add-comment", {
                method: "POST",
                body: formData
            })

            const result = await response.json();

            if (response.ok){
                showPopup("Коментарий опубликован", true);
            }
            else if (response.status === 403){
                showPopup("Коментарий не опубликован, войдите в аккаунт.", true);
            }
        }
        catch (error){
            console.log(error)
            showPopup("Коментарий не опубликован", false);
        }
    });
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