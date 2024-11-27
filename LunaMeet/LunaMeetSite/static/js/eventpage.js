document.addEventListener('DOMContentLoaded', async () => {
    const form = document.getElementById('form');
    const commentInput = document.getElementById('commentInput');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        if (!commentInput.value.trim()) {
            showPopup("Комментарий не может быть пустым.", false);
            return;
        }

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
                window.location.reload();
            }
            else if (response.status === 403){
                showPopup("Коментарий не опубликован, войдите в аккаунт.", true);
            }
        }
        catch (error){
            showPopup("Коментарий не опубликован", false);
        }
    });



    const select = document.getElementById('select');
    const response = await fetch("user-details-by-token", {
        headers: {
            "Authorization": sessionStorage.getItem("authToken")
        }
    })

    const result = await response.json();

    if (response.ok){
        select.value = result.mark;
    }
    else {
        select.value = "Не был(а)"
    }
    select.addEventListener('change', async (event) => {
        const choice = select.value;
        const parts = window.location.href.split("/");
        const event_id = parts[parts.length - 1];
        console.log(choice)
        console.log(event_id)
        console.log(sessionStorage.getItem("authToken"))

        try{
            const response = await fetch('mark-event', {
                method: "POST",
                body: JSON.stringify({
                    event_id: event_id,
                    value: choice
                }),
                headers: {
                    "Authorization": sessionStorage.getItem("authToken")
                }
            }); 

            const result = await response.json();

            if (response.ok) {
                showPopup("Значение установленно.", true);
            }
            else if (response.status === 403){
                windows.location.href = "sign-in";
            }
            else if (response.status === 404){
                console.log(result.message)
            }
        }
        catch (error) {
            showPopup("Ошибка сервера", false);
            console.log(error.message);
        }
    })
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