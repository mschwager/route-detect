<?php

use Illuminate\Support\Facades\Route;
 
// ruleid: laravel-route-unauthenticated
Route::get('/greeting', function () {
    return 'Hello World';
});

// ruleid: laravel-route-authenticated
Route::get('/greeting', function () {
    return 'Hello World';
})->middleware('auth');

// ruleid: laravel-route-authenticated
Route::get('/greeting', function () {
    return 'Hello World';
})->middleware('auth:admin');

// ruleid: laravel-route-authorized
Route::get('/greeting', function () {
    return 'Hello World';
})->middleware('can:create,App\Models\Post');

// ruleid: laravel-route-authorized
Route::get('/greeting', function () {
    return 'Hello World';
})->can('create', Post::class);
