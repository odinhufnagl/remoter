import React from "react";
import { Link, Location, matchPath } from "react-router-dom";
import { NavigationItem } from "../Layout";
import { useAuth } from "@/providers/AuthProvider";

type MenuItemProps = {
  item: NavigationItem;
  location: Location;
};

const MenuItem = ({ item, location }: MenuItemProps) => {
  const isActive = item.matchedPaths.some((path) =>
    matchPath(path, location.pathname)
  );

  return (
    <div style={{ backgroundColor: isActive ? "red" : "transparent" }}>
      <Link
        to={item.href}
        className={`block py-2 px-2 rounded ${isActive ? "bg-gray-100" : ""}`}
      >
        {item.title}
      </Link>
    </div>
  );
};

type SidebarProps = {
  items: NavigationItem[];
  location: Location;
};

const Sidebar = ({ items, location }: SidebarProps) => {
  const { logout } = useAuth();

  return (
    <aside className="h-screen w-64 p-4 border-r flex flex-col justify-between">
      <div>
        <div className="mb-4 text-xl font-bold">MyApp</div>
        <nav>
          <ul className="space-y-2">
            {items.map((item) => (
              <li key={item.id}>
                <MenuItem item={item} location={location} />
              </li>
            ))}
          </ul>
        </nav>
      </div>
      <button
        onClick={logout}
        className="py-2 px-2 bg-red-500 text-white rounded"
      >
        Logout
      </button>
    </aside>
  );
};

export default Sidebar;
