<?php

namespace App\Controller;

use App\Controller\BlogApiController;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Routing\Annotation\Route as RouteAttribute;
use Symfony\Component\Routing\Loader\Configurator\RoutingConfigurator;
use Symfony\Component\Routing\Route;
use Symfony\Component\Routing\RouteCollection;

class BlogController extends AbstractController
{
    // ruleid: symfony-route-unauthenticated
    #[RouteAttribute('/blog', name: 'blog_list')]
    public function list(): Response
    {
        // ...
    }

    /**
     // ruleid: symfony-route-unauthenticated-annotation
     * @Route("/")
     */
    public function index()
    {
        // ...
    }
}

return function (RoutingConfigurator $routes) {
    // ruleid: symfony-route-unauthenticated
    $routes->add('api_post_show', '/api/posts/{id}')
        ->controller([BlogApiController::class, 'show'])
        ->methods(['GET', 'HEAD']);

    // ruleid: symfony-route-unauthenticated
    $routes->add('api_post_edit', '/api/posts/{id}')
        ->controller([BlogApiController::class, 'edit'])
        ->methods(['PUT']);
};

function test()
{
    $routeCollection = new RouteCollection();

    // ruleid: symfony-route-unauthenticated
    $routeCollection->add('test', new Route('/path', [
        'foo' => 'Bar',
    ]));
}
