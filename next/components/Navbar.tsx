// components/Navbar.tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { name: "Home", href: "/" },
  { name: "Tasks", href: "/tasks" },
  { name: "Health", href: "/health" },
  { name: "Assistant", href: "/assistant" },
  { name: "Finance", href: "/finance" },
];

export default function Navbar() {
  const pathname = usePathname();
  return (
    <nav className="bg-gray-900 text-white p-4 shadow-md">
      <div className="max-w-6xl mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold">🤖 AIDPA</h1>
        <ul className="flex gap-6">
          {navItems.map(({ name, href }) => (
            <li key={href}>
              <Link
                href={href}
                className={`hover:text-blue-400 ${
                  pathname === href ? "text-blue-400 underline" : ""
                }`}
              >
                {name}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}
