document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.create-btn').addEventListener('click', function() {
        window.location.href = 'add-event';
    });

    const search_input = document.getElementById('search-input');
    const search_button = document.getElementById('search-btn');
    search_button.addEventListener('click', () => {
        window.location.href = `search?query=${search_input.value}`
    })
})