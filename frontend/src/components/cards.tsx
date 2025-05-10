import React from "react";

export function DashboardCards() {
  const cards = [
    {
      id: 1,
      title: "Agent Generator",
      description: "Configure and generate your passive income agent.",
      link: "/generator",
      color: "bg-purple-100 dark:bg-purple-900",
      borderColor: "border-purple-500"
    },
    {
      id: 2,
      title: "Mind Map View",
      description: "Visualize the agent generation process and configuration.",
      link: "/mindmap",
      color: "bg-orange-100 dark:bg-orange-900",
      borderColor: "border-orange-500"
    },
    {
      id: 3,
      title: "Sandbox",
      description: "Test agent configurations and strategies interactively.",
      link: "/sandbox",
      color: "bg-green-100 dark:bg-green-900",
      borderColor: "border-green-500"
    },
    {
      id: 4,
      title: "Pinterest Strategy",
      description: "Generate and manage Pinterest marketing strategies.",
      link: "/pinterest",
      color: "bg-red-100 dark:bg-red-900",
      borderColor: "border-red-500"
    },
    {
      id: 5,
      title: "Debug Tool",
      description: "Check your configuration for potential errors.",
      link: "/debug",
      color: "bg-blue-100 dark:bg-blue-900",
      borderColor: "border-blue-500"
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {cards.map((card) => (
        <a
          key={card.id}
          href={card.link}
          className={`p-6 rounded-lg border-2 ${card.borderColor} ${card.color} hover:shadow-lg transition-shadow`}
        >
          <h3 className="text-xl font-bold mb-2">{card.title}</h3>
          <p className="text-gray-700 dark:text-gray-300">{card.description}</p>
        </a>
      ))}
    </div>
  );
}
