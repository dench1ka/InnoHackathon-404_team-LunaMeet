const form = document.getElementById("form")

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(form);

    try {
        const response = await fetch('http://127.0.0.1:8000/user-sign-up', {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            window.location.href = 'http://127.0.0.1:8000/sign-in';
        } else {
            alert(result.error || "Something went wrong.");
        }
    } catch (error) {
        alert("An unexpected error occurred.");
    }
})