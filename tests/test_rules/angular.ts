import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

const routes: Routes = [
    {
        // ruleid: angular-route-authorized
        path: 'first-component',
        component: FirstComponent,
        canActivate: [componentGuard]
    },
    {
        // ruleid: angular-route-unauthorized
        path: 'second-component',
        component: SecondComponent
    },
    {
        // ruleid: angular-route-authorized
        path: 'home',
        loadChildren: () => import('./+home/home.module').then(m => m.HomeModule),
        canActivateChild: [MetaGuard]
    },
    {
        // todoruleid: angular-route-authorized, angular-route-unauthorized
        path: 'redirect-component',
        redirectTo: 'first-component',
        pathMatch: 'full',
    },
];

const routes: Routes = [
    {
        // ruleid: angular-route-authorized
        path: 'first-component',
        component: FirstComponent,
        canActivateChild: [componentGuard],
        children: [
            {
                // ruleid: angular-route-authorized
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
