<?php

$logFilePath = 'var/log/ss/remove_log.txt';

function logMessage($message) {
    global $logFilePath;
    $timestamp = date('Y-m-d H:i:s');
    $ipAddress = $_SERVER['REMOTE_ADDR'];
    $userAgent = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : 'Unknown';

    $logMessage = "$timestamp - IP: $ipAddress, User-Agent: $userAgent - $message\n";
    file_put_contents($logFilePath, $logMessage, FILE_APPEND);
}

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

        // Log the removal
        logMessage("Removed name: $nameToRemove");

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
