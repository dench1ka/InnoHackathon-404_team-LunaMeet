// Обработчик клика по кнопке "Создать объявление"
document.querySelector('.create-btn').addEventListener('click', function() {
    // Переход на страницу добавления события
    window.location.href = 'add-event'; // Замените на путь к странице добавления события
});

// Находим кнопку по ID
document.getElementById('login-button').addEventListener('click', function() {
    // Перенаправляем на страницу логина
    window.location.href = '/sign-in'; // Замените '/login' на правильный URL для вашей страницы логина
});

document.addEventListener('DOMContentLoaded', function () {
    const search_btn = document.getElementById('search-btn');
    search_btn.addEventListener('click', () => {
        const search_inp = document.getElementById('search-input');
        window.location.href = 'search?query=' + search_inp.value;

    });

    document.getElementById('login-btn').addEventListener('click', function() {
        window.location.href = '/sign-in';
    });

    })


    const authToken = sessionStorage.getItem('authToken');
    const actionsContainer = document.querySelector('.actions');
    
    if (authToken) {
      // Если пользователь авторизован
      const profileButton = document.createElement('button');
      profileButton.classList.add('profile-btn');
      profileButton.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20">
          <circle cx="12" cy="12" r="10"></circle>
          <circle cx="12" cy="10" r="3"></circle>
          <path d="M12 13c-2.67 0-8 1.34-8 4v1h16v-1c0-2.66-5.33-4-8-4z"></path>
        </svg>
      `;
      profileButton.addEventListener('click', function () {
        // Переход на страницу профиля
        window.location.href = "users/" + sessionStorage.getItem("authToken");
      });
  
      // Удаляем кнопку "Вход" и заменяем её на иконку профиля
      const loginButton = document.querySelector('.actions button:nth-child(2)');
      if (loginButton) {
        actionsContainer.removeChild(loginButton);
      }
      actionsContainer.appendChild(profileButton);
    }
  
    // Добавляем обработчик для кнопки "Создать объявление"
    const createButton = document.querySelector('.create-btn');
    if (createButton) {
      createButton.addEventListener('click', function () {
        if (authToken) {
          window.location.href = 'add-event'; // Укажите путь к добавлению события
        } else {
          alert('Пожалуйста, войдите в систему, чтобы создать объявление.');

          window.location.href = "sign-in"


        }
      });
    }

  document.addEventListener('DOMContentLoaded', function () {
    const actionsContainer = document.querySelector('.actions');

    // Проверяем наличие токена (например, из cookies или localStorage)
    const token = document.cookie.split('; ').find(row => row.startsWith('auth_token='));
    if (token) {
        // Отправляем запрос к API для получения информации о пользователе
        fetch('/api/user-info', {
            headers: {
                'Authorization': `Bearer ${token.split('=')[1]}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.username && data.avatar_url) {
                // Удаляем кнопку "Вход"
                const loginButton = document.querySelector('.actions button:nth-child(2)');
                if (loginButton) {
                    actionsContainer.removeChild(loginButton);
                }

                // Создаем элементы профиля
                const profileContainer = document.createElement('div');
                profileContainer.className = 'profile-container';

                const avatar = document.createElement('img');
                avatar.src = data.avatar_url;
                avatar.alt = 'Avatar';
                avatar.className = 'profile-avatar';

                const username = document.createElement('span');
                username.textContent = data.username;
                username.className = 'profile-username';

                profileContainer.appendChild(avatar);
                profileContainer.appendChild(username);

                // Добавляем контейнер профиля в actionsContainer
                actionsContainer.appendChild(profileContainer);
            }
        })
        .catch(error => {
            console.error('Ошибка при получении информации о пользователе:', error);
        });
    }
});