<?php

$jsonFile = 'names.json';
$removeLogFile = 'var/log/remove_log.txt';

// Load names from the JSON file
$names = json_decode(file_get_contents($jsonFile), true);

// Handle POST request to remove a name
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $postData = json_decode(file_get_contents('php://input'), true);

    if (isset($postData['nameToRemove'])) {
        $nameToRemove = $postData['nameToRemove'];

        // Remove only one instance of the selected name
        $index = array_search($nameToRemove, $names);
        if ($index !== false) {
            array_splice($names, $index, 1);
        }

        // Save the updated names back to the JSON file
        file_put_contents($jsonFile, json_encode($names));

        // Log the removed name to remove_log.txt
        file_put_contents($removeLogFile, date('Y-m-d H:i:s') . ' - ' . $nameToRemove . PHP_EOL, FILE_APPEND);

        // Return a response (you might want to customize this based on your needs)
        echo json_encode(['success' => true]);
        exit;
    }
}

// Handle GET request to fetch all names
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    header('Content-Type: application/json');
    echo json_encode($names);
    exit;
}
