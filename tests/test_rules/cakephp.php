<?php

use Cake\Routing\RouteBuilder;
use Cake\Routing\Route\DashedRoute;
use Cake\Controller\Controller;
use Cake\Http\MiddlewareQueue;
use Cake\Http\BaseApplication;

use Authentication\AuthenticationServiceProviderInterface;
use Authentication\Middleware\AuthenticationMiddleware;

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

class AppController extends Controller
{
    public function initialize()
    {
        parent::initialize();

        // ruleid: cakephp-route-global-authenticated
        $this->loadComponent('Auth', [
            'authenticate' => [
                'Form' => [
                    'fields' => ['username' => 'email', 'password' => 'passwd']
                ]
            ]
        ]);
    }
}

class Application extends BaseApplication implements AuthenticationServiceProviderInterface
{
    public function middleware(MiddlewareQueue $middlewareQueue): MiddlewareQueue
    {
        // ruleid: cakephp-route-global-authenticated
        $middlewareQueue->add(new ErrorHandlerMiddleware(Configure::read('Error')))
            ->add(new AssetMiddleware())
            ->add(new RoutingMiddleware($this))
            ->add(new BodyParserMiddleware())
            ->add(new AuthenticationMiddleware($this));

        return $middlewareQueue;
    }
}
