document.addEventListener('DOMContentLoaded', function () {
    const search_btn = document.getElementById('search-btn');
    search_btn.addEventListener('click', () => {
        const search_inp = document.getElementById('search-input');
        window.location.href = 'search?query=' + search_inp.value;

    });

    document.getElementById('login-btn').addEventListener('click', function() {
        window.location.href = '/sign-in';
    });

    const authToken = sessionStorage.getItem('authToken');
    const actionsContainer = document.querySelector('.actions');
    
    if (authToken) {
      const profileButton = document.createElement('button');
      profileButton.classList.add('profile-btn');
      profileButton.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20">
          <circle cx="12" cy="12" r="10"></circle>
          <circle cx="12" cy="10" r="3"></circle>
          <path d="M12 13c-2.67 0-8 1.34-8 4v1h16v-1c0-2.66-5.33-4-8-4z"></path>
        </svg>
        `
      profileButton.addEventListener('click', function () {
        window.location.href = "users/" + sessionStorage.getItem("authToken");
      });

      const loginButton = document.querySelector('.actions button:nth-child(2)');
      if (loginButton) {
        actionsContainer.removeChild(loginButton);
      }
      actionsContainer.appendChild(profileButton);
    }

    const createButton = document.querySelector('.create-btn');
    if (createButton) {
      createButton.addEventListener('click', function () {
        if (authToken) {
          window.location.href = 'add-event';
        } else {
          window.location.href = "sign-in"
        }
      });
    }
}); 