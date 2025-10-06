import React from 'react';
import { ExternalLink, Play } from 'lucide-react';
import { DEMO_LINKS, DEMO_DESCRIPTIONS, getDemoLink } from '../config/demoLinks';

interface DemoButtonProps {
  demoKey: keyof typeof DEMO_LINKS;
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  showDescription?: boolean;
  className?: string;
  children?: React.ReactNode;
}

export const DemoButton: React.FC<DemoButtonProps> = ({
  demoKey,
  variant = 'primary',
  size = 'md',
  showDescription = false,
  className = '',
  children
}) => {
  const link = getDemoLink(demoKey);
  const description = DEMO_DESCRIPTIONS[demoKey];
  
  const baseClasses = "inline-flex items-center gap-2 rounded-lg font-semibold transition-all duration-200 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-400/50";
  
  const variantClasses = {
    primary: "bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 shadow-lg hover:shadow-xl",
    secondary: "bg-white/10 backdrop-blur-sm text-white border border-white/20 hover:bg-white/20",
    outline: "border-2 border-blue-400 text-blue-400 hover:bg-blue-400 hover:text-white"
  };
  
  const sizeClasses = {
    sm: "px-3 py-2 text-sm",
    md: "px-6 py-3 text-base",
    lg: "px-8 py-4 text-lg"
  };
  
  const iconSize = {
    sm: "w-4 h-4",
    md: "w-5 h-5", 
    lg: "w-6 h-6"
  };

  const buttonClasses = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`;
  
  const handleClick = () => {
    window.open(link, '_blank', 'noopener,noreferrer');
  };

  return (
    <div className="demo-button-container">
      <button 
        onClick={handleClick}
        className={buttonClasses}
        disabled={link === "#"}
      >
        <Play className={iconSize[size]} />
        {children || "Подивитись демо"}
        <ExternalLink className={iconSize[size]} />
      </button>
      
      {showDescription && description && (
        <p className="text-sm text-gray-400 mt-2 max-w-md">
          {description}
        </p>
      )}
    </div>
  );
};

// Preset demo buttons for common use cases
export const AnalysisReportButton: React.FC<Omit<DemoButtonProps, 'demoKey'>> = (props) => (
  <DemoButton {...props} demoKey="COMPETITOR_ANALYSIS_REPORT">
    📊 Звіт з аналізу
  </DemoButton>
);

export const ChatDemoButton: React.FC<Omit<DemoButtonProps, 'demoKey'>> = (props) => (
  <DemoButton {...props} demoKey="CHAT_DEMO">
    💬 Демо чату
  </DemoButton>
);

export const PolicyReportButton: React.FC<Omit<DemoButtonProps, 'demoKey'>> = (props) => (
  <DemoButton {...props} demoKey="POLICY_REPORT">
    🛡️ Policy звіт
  </DemoButton>
);

export const VideoDemoButton: React.FC<Omit<DemoButtonProps, 'demoKey'>> = (props) => (
  <DemoButton {...props} demoKey="VIDEO_DEMO">
    🎥 Демо відео
  </DemoButton>
);

export const ApiDocsButton: React.FC<Omit<DemoButtonProps, 'demoKey'>> = (props) => (
  <DemoButton {...props} demoKey="API_DOCS">
    📚 API Docs
  </DemoButton>
);
