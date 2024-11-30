// Существующие элементы
const loginButton = document.getElementById('loginButton');
const modal = document.getElementById('modal');
const closeModal = document.getElementById('closeModal');
const registerModal = document.getElementById('registerModal');
const closeRegisterModal = document.getElementById('closeRegisterModal');
const registerLink = document.getElementById('registerLink');

// Новый элемент: кнопка "Профиль"
const profileButton = document.getElementById('profileButton');

// Открытие страницы профиля в новом окне
profileButton.onclick = () => {
  window.open('profile.html', '_blank');
};

// Открытие модального окна для входа
loginButton.onclick = () => {
  modal.style.display = 'flex';
};

// Закрытие модального окна для входа
closeModal.onclick = () => {
  modal.style.display = 'none';
};

// Открытие окна регистрации
registerLink.onclick = (e) => {
  e.preventDefault();
  modal.style.display = 'none';
  registerModal.style.display = 'flex';
};

// Закрытие окна регистрации
closeRegisterModal.onclick = () => {
  registerModal.style.display = 'none';
};

// Закрытие модальных окон при клике вне их области
window.onclick = (event) => {
  if (event.target === modal) modal.style.display = 'none';
  if (event.target === registerModal) registerModal.style.display = 'none';
};
