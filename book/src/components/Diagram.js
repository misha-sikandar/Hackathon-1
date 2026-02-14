import React from 'react';
import clsx from 'clsx';

// Simple SVG-based diagram component for robotics architecture
export default function Diagram({ type, title, children, className }) {
  const diagramClasses = clsx('robot-diagram', className);

  switch (type) {
    case 'architecture':
      return (
        <div className={diagramClasses}>
          <h4>{title}</h4>
          <svg width="100%" height="200" viewBox="0 0 600 200">
            {/* Robot */}
            <rect x="50" y="80" width="60" height="80" fill="#e2e8f0" stroke="#4a5568" strokeWidth="2"/>
            <circle cx="80" cy="60" r="30" fill="#e2e8f0" stroke="#4a5568" strokeWidth="2"/>

            {/* Sensors */}
            <circle cx="60" cy="90" r="8" fill="#4299e1" stroke="#2b6cb0"/>
            <circle cx="100" cy="90" r="8" fill="#4299e1" stroke="#2b6cb0"/>
            <circle cx="80" cy="100" r="8" fill="#4299e1" stroke="#2b6cb0"/>

            {/* Perception System */}
            <rect x="200" y="50" width="100" height="60" fill="#feb2b2" stroke="#e53e3e" strokeWidth="2"/>
            <text x="250" y="80" textAnchor="middle" fontSize="12" fontWeight="bold">Perception</text>

            {/* Planning System */}
            <rect x="200" y="130" width="100" height="60" fill="#b3e6ff" stroke="#3182ce" strokeWidth="2"/>
            <text x="250" y="160" textAnchor="middle" fontSize="12" fontWeight="bold">Planning</text>

            {/* Action System */}
            <rect x="350" y="90" width="100" height="60" fill="#b3ffd9" stroke="#38a169" strokeWidth="2"/>
            <text x="400" y="120" textAnchor="middle" fontSize="12" fontWeight="bold">Action</text>

            {/* Arrows */}
            <line x1="110" y1="100" x2="200" y2="80" stroke="#4a5568" strokeWidth="2" markerEnd="url(#arrowhead)"/>
            <line x1="110" y1="140" x2="200" y2="160" stroke="#4a5568" strokeWidth="2" markerEnd="url(#arrowhead)"/>
            <line x1="300" y1="80" x2="350" y2="110" stroke="#4a5568" strokeWidth="2" markerEnd="url(#arrowhead)"/>
            <line x1="300" y1="160" x2="350" y2="130" stroke="#4a5568" strokeWidth="2" markerEnd="url(#arrowhead)"/>

            {/* Arrowhead definition */}
            <defs>
              <marker id="arrowhead" markerWidth="10" markerHeight="7"
                      refX="9" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="#4a5568" />
              </marker>
            </defs>
          </svg>
          {children}
        </div>
      );

    case 'sensor-flow':
      return (
        <div className={diagramClasses}>
          <h4>{title}</h4>
          <svg width="100%" height="150" viewBox="0 0 600 150">
            {/* Camera */}
            <rect x="50" y="50" width="40" height="50" fill="#e2e8f0" stroke="#4a5568" strokeWidth="2"/>
            <circle cx="70" cy="40" r="15" fill="#feb2b2" stroke="#e53e3e" strokeWidth="2"/>
            <text x="70" y="115" textAnchor="middle" fontSize="12">Camera</text>

            {/* LiDAR */}
            <circle cx="180" cy="75" r="25" fill="#e2e8f0" stroke="#4a5568" strokeWidth="2"/>
            <circle cx="180" cy="75" r="15" fill="#b3e6ff" stroke="#3182ce" strokeWidth="2"/>
            <text x="180" y="115" textAnchor="middle" fontSize="12">LiDAR</text>

            {/* IMU */}
            <rect x="300" y="50" width="50" height="50" fill="#e2e8f0" stroke="#4a5568" strokeWidth="2"/>
            <text x="325" y="70" textAnchor="middle" fontSize="10">IMU</text>
            <text x="325" y="85" textAnchor="middle" fontSize="8">Sensor</text>
            <text x="325" y="115" textAnchor="middle" fontSize="12">IMU</text>

            {/* Processor */}
            <rect x="420" y="40" width="80" height="70" fill="#b3ffd9" stroke="#38a169" strokeWidth="2"/>
            <text x="460" y="75" textAnchor="middle" fontSize="10" fontWeight="bold">Sensor</text>
            <text x="460" y="90" textAnchor="middle" fontSize="10" fontWeight="bold">Processor</text>
            <text x="460" y="115" textAnchor="middle" fontSize="12">Fusion</text>

            {/* Arrows */}
            <line x1="90" y1="75" x2="155" y2="75" stroke="#4a5568" strokeWidth="2" markerEnd="url(#arrowhead)"/>
            <line x1="205" y1="75" x2="300" y2="75" stroke="#4a5568" strokeWidth="2" markerEnd="url(#arrowhead)"/>
            <line x1="350" y1="75" x2="420" y2="75" stroke="#4a5568" strokeWidth="2" markerEnd="url(#arrowhead)"/>

            {/* Arrowhead definition */}
            <defs>
              <marker id="arrowhead" markerWidth="10" markerHeight="7"
                      refX="9" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="#4a5568" />
              </marker>
            </defs>
          </svg>
          {children}
        </div>
      );

    default:
      return (
        <div className={diagramClasses}>
          <h4>{title}</h4>
          {children}
        </div>
      );
  }
}