<?php

namespace App\Controller;

use App\Controller\BlogApiController;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Routing\Loader\Configurator\RoutingConfigurator;

class BlogController extends AbstractController
{
    // ruleid: symfony-route-unauthenticated
    #[Route('/blog', name: 'blog_list')]
    public function list(): Response
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
