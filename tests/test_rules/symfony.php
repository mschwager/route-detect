<?php

namespace App\Controller;

use App\Controller\BlogApiController;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Routing\Annotation\Route as RouteAttribute;
use Symfony\Component\Routing\Loader\Configurator\RoutingConfigurator;
use Symfony\Component\Routing\Route;
use Symfony\Component\Routing\RouteCollection;
use Sensio\Bundle\FrameworkExtraBundle\Configuration\Security;
use Sensio\Bundle\FrameworkExtraBundle\Configuration\IsGranted;

class BlogController extends AbstractController
{
    // ruleid: symfony-route-php
    #[RouteAttribute('/blog', name: 'blog_list')]
    public function list(): Response
    {
        // ...
    }

    /**
     // ruleid: symfony-route-annotation-unauthorized
     * @Route("/")
     */
    public function index()
    {
        // ...
    }

    /**
     // ruleid: symfony-route-annotation-authorized
     * @Route("/")
     * @IsGranted("ROLE_ADMIN")
     */
    public function index()
    {
        // ...
    }

    /**
     // ruleid: symfony-route-annotation-authorized
     * @Route("/")
     * @Security("is_granted('ROLE_ADMIN') and is_granted('ROLE_FRIENDLY_USER')")
     */
    public function index()
    {
        // ...
    }
}

return function (RoutingConfigurator $routes) {
    // ruleid: symfony-route-php
    $routes->add('api_post_show', '/api/posts/{id}')
        ->controller([BlogApiController::class, 'show'])
        ->methods(['GET', 'HEAD']);

    // ruleid: symfony-route-php
    $routes->add('api_post_edit', '/api/posts/{id}')
        ->controller([BlogApiController::class, 'edit'])
        ->methods(['PUT']);
};

function test()
{
    $routeCollection = new RouteCollection();

    // ruleid: symfony-route-php
    $routeCollection->add('test', new Route('/path', [
        'foo' => 'Bar',
    ]));
}
