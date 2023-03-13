import * as React from "react";
import { Routes, Route, Outlet, Link } from "react-router-dom";

export default function App() {
  return (
    <div>
      <h1>Basic Example</h1>
      <Routes>
        // ruleid: react-route
        <Route path="/" element={<Layout />}>
          // ok: react-route
          <Route index element={<Home />} />
          // ruleid: react-route
          <Route path="about" element={<About />} />
          // ruleid: react-route
          <Route path="dashboard" element={<Dashboard />} />
          // ruleid: react-route
          <Route path="*" element={<NoMatch />} />
        </Route>
      </Routes>
    </div>
  );
}
