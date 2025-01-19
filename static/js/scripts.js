document.getElementById('quizForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const answers = {};
    formData.forEach((value, key) => answers[key] = value);

    fetch(`/quiz/${event.target.dataset.moduleName}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(answers)
    }).then(response => response.json()).then(data => {
        alert('Quiz submitted successfully!');
    });
});
