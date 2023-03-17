import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, createRoutesFromElements } from "react-router-dom";

const router = createBrowserRouter([
  // ruleid: react-route-unauthenticated
  {
    path: "/",
    element: <div>Hello world!</div>,
  },
  // ruleid: react-route-authenticated
  {
    path: "/",
    element: <ProtectedRoute><div>Hello world!</div></ProtectedRoute>,
  },
  // ruleid: react-route-authenticated
  {
    path: "/",
    element: <RequireAuth><div>Hello world!</div></RequireAuth>,
  },
  // ruleid: react-route-authenticated
  {
    path: "/",
    element: <AuthenticationGuard component={ProfilePage} />,
  },
]);

const router = createBrowserRouter(
  createRoutesFromElements(
    // ruleid: react-route-unauthenticated
    <Route
      path="/"
      element={<Root />}
      loader={rootLoader}
      action={rootAction}
      errorElement={<ErrorPage />}
    >
      // ok: react-route-authenticated
      <Route errorElement={<ErrorPage />}>
        // ok: react-route-authenticated
        <Route index element={<Index />} />
        // ruleid: react-route-authenticated
        <Route
          path="contacts/:contactId"
          element={<ProtectedRoute><Contact /></ProtectedRoute>}
          loader={contactLoader}
          action={contactAction}
        />
        // ruleid: react-route-authenticated
        <Route
          path="contacts/:contactId/edit"
          element={<RequireAuth><EditContact /></RequireAuth>}
          loader={contactLoader}
          action={editAction}
        />
        // ruleid: react-route-authenticated
        <Route
          path="contacts/:contactId/edit"
          element={<Protected><EditContact /></Protected>}
          loader={contactLoader}
          action={editAction}
        />
        // ruleid: react-route-authenticated
        <Route
          path="/profile"
          element={<AuthenticationGuard component={ProfilePage} />}
        />
        // ruleid: react-route-unauthenticated
        <Route
          path="contacts/:contactId/destroy"
          action={destroyAction}
        />
        // ruleid: react-route-authenticated
        <ProtectedRoute path="/external-api" component={ExternalApi} />
      </Route>
    </Route>
  )
);
