// Модальные окна
const loginButton = document.getElementById('loginButton');
const modal = document.getElementById('modal');
const registerModal = document.getElementById('registerModal');
const eventModal = document.getElementById('eventModal');
const closeModal = document.getElementById('closeModal');
const closeRegisterModal = document.getElementById('closeRegisterModal');
const closeEventModal = document.getElementById('closeEventModal');
const registerLink = document.getElementById('registerLink');
const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const eventsContainer = document.getElementById('eventsContainer');

// События
const events = [
  { title: "Innowsie Hackaton", date: "22.11.2024 - 23.11.2024", location: "Gomel" },
  { title: "CodeFest 2024", date: "12.12.2024 - 13.12.2024", location: "Minsk" },
  { title: "Design Sprint", date: "15.01.2025", location: "Minsk" },
  { title: "AI Summit", date: "20.02.2025 - 21.02.2025", location: "Gomel" },
];

// Генерация карточек
function renderEvents(eventsToRender) {
  eventsContainer.innerHTML = "";
  eventsToRender.forEach((event) => {
    const card = document.createElement("div");
    card.classList.add("card");
    card.innerHTML = `
      <div class="image"></div>
      <div class="info">
        <h3>${event.title}</h3>
        <p>${event.date}</p>
        <p>${event.location}</p>
      </div>`;
    card.onclick = () => openEventCard(event.title, event.date, event.location);
    eventsContainer.appendChild(card);
  });
}

renderEvents(events);

// Поиск событий
searchButton.onclick = () => {
  const query = searchInput.value.toLowerCase();
  const filteredEvents = events.filter(event =>
    event.title.toLowerCase().includes(query) ||
    event.location.toLowerCase().includes(query)
  );
  renderEvents(filteredEvents);
};

// Открытие модального окна события
function openEventCard(title, date, location) {
  document.getElementById('eventTitle').innerText = title;
  document.getElementById('eventDate').innerText = date;
  document.getElementById('eventLocation').innerText = location;
  eventModal.style.display = 'flex';
}

// Открытие и закрытие модальных окон
loginButton.onclick = () => (modal.style.display = 'flex');
closeModal.onclick = () => (modal.style.display = 'none');
closeRegisterModal.onclick = () => (registerModal.style.display = 'none');
closeEventModal.onclick = () => (eventModal.style.display = 'none');
registerLink.onclick = (e) => {
  e.preventDefault();
  modal.style.display = 'none';
  registerModal.style.display = 'flex';
};

window.onclick = (event) => {
  if (event.target === modal) modal.style.display = 'none';
  if (event.target === registerModal) registerModal.style.display = 'none';
  if (event.target === eventModal) eventModal.style.display = 'none';
};


// Переход на страницу мероприятия
function openEvent() {
    window.location.href = 'event.html';
}

// Получаем элементы
const registerButton = document.querySelector('.btn-register');
const closeRegisterModal = document.getElementById('closeRegisterModal');

// Открытие модального окна
registerButton.onclick = () => {
  registerModal.style.display = 'flex';
};

// Закрытие модального окна
closeRegisterModal.onclick = () => {
  registerModal.style.display = 'none';
};

// Закрытие модального окна при клике вне его
window.onclick = (event) => {
  if (event.target === registerModal) {
    registerModal.style.display = 'none';
  }
};