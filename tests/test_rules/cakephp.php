<?php

use Cake\Routing\RouteBuilder;
use Cake\Routing\Route\DashedRoute;

$routes->scope('/', function (RouteBuilder $routes) {
    // ruleid: cakephp-route-unauthenticated
    $routes->connect('/articles/*', ['controller' => 'Articles', 'action' => 'view']);

    // ruleid: cakephp-route-unauthenticated
    $routes->get(
        '/cooks/{id}',
        ['controller' => 'Users', 'action' => 'view'],
        'users:view'
    );

    // ruleid: cakephp-route-unauthenticated
    $routes->fallbacks(DashedRoute::class);
});
