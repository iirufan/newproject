<?php
$photoFolder = 'static/img';
$photos = [];

// Get all files in the folder
$files = glob($photoFolder . '*.{jpg,jpeg,png,gif}', GLOB_BRACE);

// Create an array of photo URLs
foreach ($files as $file) {
    $photos[] = $file;
}

// Return the array as JSON
echo json_encode($photos);
?>