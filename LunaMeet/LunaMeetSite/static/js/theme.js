document.addEventListener('DOMContentLoaded', () => {
    const themeToggleButton = document.getElementById('theme-toggle');
    const themeIcon = themeToggleButton?.querySelector('img');
    const logoImg = document.getElementById('logo');
    const theme = document.getElementById('dark-mode-icon');
    const backgroundContent = document.getElementById('content');
    const backgroundBlock = document.getElementById('block');
    const backgroundButton = document.getElementById('btn');
    const header = document.getElementById('header');
    const textElements = document.querySelectorAll('.text'); // Все элементы с классом текста
    const cards = document.querySelectorAll('.card');
    const owner = document.getElementById('owner');
    const img = document.getElementById('image');

    const comments = document.querySelectorAll('.comment')

    // Функция для включения тёмной темы
    function enableDarkTheme() {
        document.body.classList.add('dark-theme');
        themeIcon?.setAttribute('src', '../static/img/sun.png');
        if (logoImg) logoImg.src = '../static/img/LunaMeet_white_without_background.png';
        theme?.setAttribute('src', '../static/img/Night.png');
        header?.style.setProperty('background', '#2C2F36');
        backgroundContent?.style.setProperty('background', '#1B1D23');
        backgroundBlock?.style.setProperty('background', '#2C2F36');
        owner?.style.setProperty('background','#2C2F36');
        img?.style.setProperty('background','#2C2F36');
        if (backgroundButton) {
            backgroundButton.style.setProperty('background', '#2979FF');
            backgroundButton.style.setProperty('color', '#fff');
        }
        textElements.forEach(el => el.style.setProperty('color', '#fff'));
        cards.forEach(card => card.style.setProperty('background', '#2C2F36'));
        comments?.forEach(comment => comment.style.setProperty('background','#2C2F36'));
        if (backgroundBlock) backgroundBlock.style.setProperty('background-color', '#11141A');
    }

    // Функция для включения светлой темы
    function enableLightTheme() {
        document.body.classList.remove('dark-theme');
        themeIcon?.setAttribute('src', '../static/img/moon.png');
        if (logoImg) logoImg.src = '../static/img/LunaMeet_without_background.png';
        theme?.setAttribute('src', '../static/img/Day.png');
        header?.style.setProperty('background', '#E5F3FF');
        backgroundContent?.style.setProperty('background', '#FFFFFF');
        backgroundBlock?.style.setProperty('background', '#E5F3FF');
        owner?.style.setProperty('background','#d9d9d9');
        img?.style.setProperty('background','#d9d9d9');
        if (backgroundButton) {
            backgroundButton.style.setProperty('background', '#2979FF');
            backgroundButton.style.setProperty('color', '#fff');
        }
        textElements.forEach(el => el.style.setProperty('color', '#000'));
        cards.forEach(card => card.style.setProperty('background', '#fff'));
        comments?.forEach(comment => comment.style.setProperty('background','#d9d9d9'));
        if (backgroundBlock) backgroundBlock.style.setProperty('background-color', '#f0f0f0');
    }

    // Применить тему из localStorage
    function applyThemeFromLocalStorage() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') enableDarkTheme();
        else enableLightTheme();
    }

    // Установить тему при загрузке страницы
    applyThemeFromLocalStorage();

    // Переключение темы
    themeToggleButton?.addEventListener('click', () => {
        const isDarkTheme = document.body.classList.toggle('dark-theme');
        localStorage.setItem('theme', isDarkTheme ? 'dark' : 'light');
        if (isDarkTheme) enableDarkTheme();
        else enableLightTheme();
    });

    // Реакция на изменения в localStorage для синхронизации между вкладками
    window.addEventListener('storage', (event) => {
        if (event.key === 'theme') {
            applyThemeFromLocalStorage();
        }
    });
});
