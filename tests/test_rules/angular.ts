import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

const routes: Routes = [
    {
        // ruleid: angular-route-authenticated
        path: 'first-component',
        component: FirstComponent,
        canActivate: [componentGuard]
    },
    {
        // ruleid: angular-route-unauthenticated
        path: 'second-component',
        component: SecondComponent
    },
    {
        // ruleid: angular-route-authenticated
        path: 'home',
        loadChildren: () => import('./+home/home.module').then(m => m.HomeModule),
        canActivateChild: [MetaGuard]
    },
    {
        // todoruleid: angular-route-authenticated, angular-route-unauthenticated
        path: 'redirect-component',
        redirectTo: 'first-component',
        pathMatch: 'full',
    },
];

const routes: Routes = [
    {
        // ruleid: angular-route-authenticated
        path: 'first-component',
        component: FirstComponent,
        canActivateChild: [componentGuard],
        children: [
            {
                // ruleid: angular-route-authenticated
                path: 'second-component',
                component: SecondComponent
            },
        ],
    },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
