import React from "react";

import Sidebar from "./components/Sidebar";

import { ReactNode } from "react";
import { useLocation } from "react-router-dom";

export type NavigationItem = {
  id: string;
  href: string;
  title: string;
  matchedPaths: string[];
  subItems?: NavigationItem[];
};

export const navigationItems: NavigationItem[] = [
  {
    id: "dashboard",
    title: "Dashboard",
    href: "/app/dashboard",
    matchedPaths: ["/app/dashboard"],
  },
  {
    id: "settings",
    title: "Settings",
    href: "/app/settings",
    matchedPaths: ["/app/settings"],
  },
];

export const Layout = ({ children }: { children: ReactNode }) => {
  const location = useLocation();

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <Sidebar items={navigationItems} location={location} />
      <main style={{ flex: 1 }}>{children}</main>
    </div>
  );
};
