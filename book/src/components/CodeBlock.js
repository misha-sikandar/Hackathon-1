import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

// Enhanced code block component for robotics examples
export default function CodeBlock({ children, language, title, description }) {
  return (
    <div className="simulation-code-block">
      {title && <h5>{title}</h5>}
      {description && <p><em>{description}</em></p>}
      <pre style={{ margin: 0, padding: '1rem' }}>
        <code className={`language-${language}`}>
          {children}
        </code>
      </pre>
    </div>
  );
}