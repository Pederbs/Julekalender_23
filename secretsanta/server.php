<?php

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // Handle GET request to retrieve names
    $names = json_decode(file_get_contents('names.json'), true);
    echo json_encode($names);
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Handle POST request to remove a name
    $postData = json_decode(file_get_contents('php://input'), true);

    if (isset($postData['nameToRemove'])) {
        $nameToRemove = $postData['nameToRemove'];

        $names = json_decode(file_get_contents('names.json'), true);

        // Remove the specified name
        $names = array_values(array_diff($names, [$nameToRemove]));

        // Update the JSON file
        file_put_contents('names.json', json_encode($names, JSON_PRETTY_PRINT));

        echo json_encode(['success' => true]);
    } else {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid request']);
    }
} else {
    http_response_code(405);
    echo json_encode(['error' => 'Method Not Allowed']);
}
?>
