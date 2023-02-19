<?php

use Cake\Routing\RouteBuilder;
use Cake\Routing\Route\DashedRoute;

$routes->scope('/', function (RouteBuilder $routes) {
    // ruleid: cakephp-route
    $routes->connect('/articles/*', ['controller' => 'Articles', 'action' => 'view']);

    // ruleid: cakephp-route
    $routes->get(
        '/cooks/{id}',
        ['controller' => 'Users', 'action' => 'view'],
        'users:view'
    );

    // ruleid: cakephp-route
    $routes->fallbacks(DashedRoute::class);
});
