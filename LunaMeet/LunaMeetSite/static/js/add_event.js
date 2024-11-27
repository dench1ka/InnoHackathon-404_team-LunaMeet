document.addEventListener('DOMContentLoaded', function() {
    // Функция добавления организатора
    document.getElementById('addOrganizer').addEventListener('click', async function() {
        var organizerInput = document.getElementById('organizerInput');
        var organizerName = organizerInput.value.trim();

        const response = await fetch(`http://127.0.0.1:8000/api-user-by-username?username=${organizerName}`, {
            method: "GET",
        });

        const result = await response.json();

        if (organizerName && response.ok) {
            var listItem = document.createElement('li');
            listItem.textContent = organizerName;
            var removeButton = document.createElement('button');
            removeButton.textContent = 'Удалить';
            removeButton.addEventListener('click', function() {
                listItem.remove();
            });
            listItem.appendChild(removeButton);
            document.getElementById('organizerList').appendChild(listItem);
            organizerInput.value = '';  // Очищаем поле ввода после добавления
        } else if (organizerName) {
            showPopup(result.error, false);
        }
    });

    // Функция добавления временной метки
    document.getElementById('addTimecod').addEventListener('click', function() {
        var timecodName = document.getElementById('timecodName').value.trim();
        var timecodDate = document.getElementById('timecodDate').value;

        if (timecodName && timecodDate) {
            var listItem = document.createElement('li');
            listItem.textContent = `${timecodName} - ${timecodDate}`;
            var removeButton = document.createElement('button');
            removeButton.textContent = 'Удалить';
            removeButton.addEventListener('click', function() {
                listItem.remove();
            });
            listItem.appendChild(removeButton);
            document.getElementById('timecodList').appendChild(listItem);
        }
    });

    // Превью изображений
    document.getElementById('images').addEventListener('change', function(event) {
        var files = event.target.files;
        var previewContainer = document.getElementById('imagePreview');
        previewContainer.innerHTML = ''; // Очищаем предыдущее превью

        for (var i = 0; i < files.length; i++) {
            var reader = new FileReader();
            reader.onload = function(fileEvent) {
                var img = document.createElement('img');
                img.src = fileEvent.target.result;
                previewContainer.appendChild(img);
            };
            reader.readAsDataURL(files[i]);
        }
    });

    const form = document.getElementById('eventForm');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        // Создаем FormData для отправки данных
        const formData = new FormData(form);

        // Добавляем организаторов в FormData
        const organizersList = document.getElementById('organizerList').getElementsByTagName('li');
        for (let item of organizersList) {
            let organizerName = item.textContent.replace('Удалить', '').trim();
            formData.append('organizers[]', organizerName);
        }

        // Добавляем временные метки в FormData
        const timecodList = document.getElementById('timecodList').getElementsByTagName('li');
        for (let item of timecodList) {
            let timecodText = item.textContent.replace('Удалить', '').trim();
            formData.append('timecods[]', timecodText);
        }

        console.log(formData);

        try {
            const response = await fetch("http://127.0.0.1:8000/api-add-event", {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                document.location.href = 'http://127.0.0.1:8000';
            } else {
                showPopup(result.error, false);
            }
        } catch (error) {
            console.log(error);
            showPopup('Ошибка при отправке данных', false);
        }
    });
});

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
