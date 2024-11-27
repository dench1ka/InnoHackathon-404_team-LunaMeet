document.addEventListener('DOMContentLoaded', () => {
    const theme = localStorage.getItem('theme') || 'dark'; // Темная тема по умолчанию
    setTheme(theme);
});

const switchThemeBtn = document.getElementById('switch-theme-btn');

// Обработчик переключения темы
switchThemeBtn.addEventListener('click', () => {
    const currentTheme = localStorage.getItem('theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
});

// Функция установки темы
function setTheme(theme) {
    const themeStyle = document.getElementById('theme-style');
    const logoImg = document.getElementById('logo');
    const themeIcon = document.getElementById('theme-icon');
    const paragraph = document.getElementById('paragraph');

    if (theme === 'light') {
        themeStyle.href = '../static/css/registration_page.css' ;
        logoImg.src = '../static/img/LunaMeet_without_background.png';
        themeIcon.src = '../static/img/moon.png'; // Иконка солнца для светлой темы
        paragraph.style.color = 'black';
    } else {
        themeStyle.href = '../static/css/registration_page_night.css';
        logoImg.src ='../static/img/LunaMeet_white_without_background.png';
        themeIcon.src ='../static/img/sun.png'; // Иконка луны для темной темы
        paragraph.style.color = 'white';
    }

    localStorage.setItem('theme', theme);
}
