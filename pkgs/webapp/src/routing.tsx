import {
  Route,
  Navigate,
  Outlet,
  BrowserRouter,
  Routes,
} from "react-router-dom";
import React from "react";

import { DashboardPage } from "./pages/app/dashboard/Dashboard.page";
import { SettingsPage } from "./pages/app/settings/Settings.page";
import { Signup } from "./pages/auth/signup/Signup.page";
import { Login } from "./pages/auth/login/Login.page";

import { authService } from "./services/AuthService";
import { AUTH_STATUS, AuthProvider, useAuth } from "./providers/AuthProvider";
import { Layout } from "./components/Layout/Layout";

const PublicRoute = () => {
  const accessToken = authService.accessToken();
  const refreshToken = authService.refreshToken();

  if (accessToken || refreshToken) {
    return <Navigate to="/app" />;
  }

  return <Outlet />;
};

const ProtectedRoute = () => {
  const accessToken = authService.accessToken();
  const refreshToken = authService.refreshToken();
  if (!accessToken && !refreshToken) {
    return <Navigate to="/login" />;
  }
  return <Outlet />;
};

const RedirectToAppropriate = () => {
  const accessToken = authService.accessToken();
  const refreshToken = authService.refreshToken();
  if (accessToken || refreshToken) {
    return <Navigate to="/app/dashboard" />;
  }
  return <Navigate to="/login" />;
};

export const AppRoutingWrapper = () => {
  const { currentUser } = useAuth();

  if (currentUser.status === AUTH_STATUS.ERROR) {
    return <div>Our servers seems to be down...</div>;
  }

  if (currentUser.status === AUTH_STATUS.NOT_AUTHENTICATED) {
    return <Navigate to="/login" />;
  }

  return (
    <Layout>
      <Outlet />
    </Layout>
  );
};

export const Routing = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PublicRoute />}>
          <Route index element={<Navigate to="/login" replace />} />
          <Route path="login" element={<Login />} />
          <Route path="signup" element={<Signup />} />
        </Route>

        <Route path="/app/*" element={<ProtectedRoute />}>
          <Route
            element={
              <AuthProvider>
                <AppRoutingWrapper />
              </AuthProvider>
            }
          >
            <Route index element={<Navigate to="/app/dashboard" replace />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="settings" element={<SettingsPage />} />
            <Route
              path="*"
              element={<Navigate to="/app/dashboard" replace />}
            />
          </Route>
        </Route>
        <Route path="*" element={<RedirectToAppropriate />} />
      </Routes>
    </BrowserRouter>
  );
};
