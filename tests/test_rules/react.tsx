import * as React from "react";
import { Routes, Route, Outlet, Link } from "react-router-dom";

export default function App() {
  return (
    <div>
      <h1>Basic Example</h1>
      <Routes>
        // ruleid: react-route-unauthenticated
        <Route path="/" element={<Layout />}>
          // ok: react-route-unauthenticated
          <Route index element={<Home />} />
          // ruleid: react-route-unauthenticated
          <Route path="about" element={<About />} />
          // ruleid: react-route-authenticated
          <Route path="dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          // ruleid: react-route-authenticated
          <Route path="admin" element={<RequireAuth><Admin /></RequireAuth>} />
          // ruleid: react-route-authenticated
          <Route path="admin" element={<Protected><Admin /></Protected>} />
          // ruleid: react-route-authenticated
          <Route path="/profile" element={<AuthenticationGuard component={ProfilePage} />} />
          // ruleid: react-route-unauthenticated
          <Route path="*" element={<NoMatch />} />
          // ruleid: react-route-authenticated
          <ProtectedRoute path="/external-api" component={ExternalApi} />
        </Route>
      </Routes>
    </div>
  );
}
