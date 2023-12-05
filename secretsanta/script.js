document.addEventListener('DOMContentLoaded', function () {
    const pickButton = document.getElementById('pickButton');
    const resultDiv = document.getElementById('result');

    pickButton.addEventListener('click', pickSecretSanta);

    function pickSecretSanta() {
        fetch('server.php', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(names => {
                if (names.length === 0) {
                    resultDiv.innerHTML = '\nAlle deltakere er trukket. God Jul!';
                } else {
                    const randomIndex = Math.floor(Math.random() * names.length);
                    const selectedName = names[randomIndex];

                    const isPresent = confirm(`Er ${selectedName} tilstede?`);

                    if (isPresent) {
                        // Notify the server to remove the selected name
                        fetch('server.php', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ nameToRemove: selectedName }),
                        })
                            .then(response => response.json())
                            .then(() => {
                                resultDiv.innerHTML = `\n${selectedName} har blitt trukket! \nKos deg med gaven!`;
                            })
                            .catch(error => console.error('Error notifying server:', error));
                    } else {
                        pickSecretSanta(); // Retry if the person is not present
                    }
                }
            })
            .catch(error => console.error('Error fetching names from server:', error));
    }
});
