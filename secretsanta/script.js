document.addEventListener('DOMContentLoaded', function () {
    const pickButton = document.getElementById('pickButton');
    const resultDiv = document.getElementById('result');
    const allNamesDiv = document.getElementById('allNames');

    pickButton.addEventListener('click', pickSecretSanta);

    // Initial display of all names when the page loads
    fetchAndDisplayAllNames();

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
                    resultDiv.innerHTML = '<br>Alle deltakere er trukket. God Jul!';
                } else {
                    const randomIndex = Math.floor(Math.random() * names.length);
                    const selectedName = names[randomIndex];

                    const isPresent = confirm(`Er ${selectedName} tilstede?`);

                    if (isPresent) {
                        // Notify the server to remove the selected name
                        removeName(selectedName);
                    } else {
                        pickSecretSanta(); // Retry if the person is not present
                    }
                }
            })
            .catch(error => console.error('Error fetching names from server:', error));
    }

    function removeName(nameToRemove) {
        fetch('server.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nameToRemove }),
        })
            .then(response => response.json())
            .then(() => {
                resultDiv.innerHTML = `<br>${nameToRemove} har blitt trukket!<br> Kos deg med gaven!`;
                // Refresh the display after removing a name
                fetchAndDisplayAllNames();
            })
            .catch(error => console.error('Error notifying server:', error));
    }

    function fetchAndDisplayAllNames() {
        fetch('server.php', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(names => {
                displayAllNames(names);
            })
            .catch(error => console.error('Error fetching names from server:', error));
    }

    function displayAllNames(names) {
        // Clear the names display
        allNamesDiv.innerHTML = '';

        // Separate identical and different names
        const { identicalNames, differentNames } = separateIdenticalNames(names || []);

        // Display identical names vertically
        identicalNames.forEach(identicalGroup => {
            const namesList = document.createElement('ul');
            identicalGroup.forEach(name => {
                const listItem = document.createElement('li');
                listItem.textContent = name;
                namesList.appendChild(listItem);
            });
            allNamesDiv.appendChild(namesList);
        });

        // Display different names side by side
        const namesList = document.createElement('ul');
        differentNames.forEach(name => {
            const listItem = document.createElement('li');
            listItem.textContent = name;
            namesList.appendChild(listItem);
        });
        allNamesDiv.appendChild(namesList);
    }

    function separateIdenticalNames(names) {
        const groupedNames = {};

        // Group names by their value
        names.forEach(name => {
            if (!groupedNames[name]) {
                groupedNames[name] = [];
            }
            groupedNames[name].push(name);
        });

        // Separate identical and different names
        const identicalNames = [];
        const differentNames = [];

        Object.values(groupedNames).forEach(group => {
            if (group.length > 1) {
                identicalNames.push(group);
            } else {
                differentNames.push(group[0]);
            }
        });

        return { identicalNames, differentNames };
    }
});
