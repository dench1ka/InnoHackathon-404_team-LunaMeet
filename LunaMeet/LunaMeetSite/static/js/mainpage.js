// Обработчик клика по кнопке "Создать объявление"
document.querySelector('.create-btn').addEventListener('click', function() {
    // Переход на страницу добавления события
    window.location.href = 'add-event'; // Замените на путь к странице добавления события
});
// Обработчик клика по кнопке "Вход"
document.getElementById('login-button').addEventListener('click', function () {
    // Перенаправляем пользователя на страницу логина
    window.location.href = 'sign-in'; // Замените '/login' на корректный URL
});

document.addEventListener('DOMContentLoaded', function () {
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
        window.location.href = 'profile'; // Укажите путь к странице профиля
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
        }
      });
    }
  });
  