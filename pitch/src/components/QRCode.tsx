import React from 'react';

interface QRCodeProps {
  url?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  position?: 'top-right' | 'bottom-right' | 'bottom-left' | 'center';
  className?: string;
  showText?: boolean;
}

export const QRCode: React.FC<QRCodeProps> = ({
  url = "https://flutter-a096c.web.app/",
  size = 'md',
  position = 'bottom-right',
  className = '',
  showText = true
}) => {
  const sizeClasses = {
    sm: 'w-16 h-16',
    md: 'w-24 h-24', 
    lg: 'w-32 h-32',
    xl: 'w-72 h-72'
  };

  const positionClasses = {
    'top-right': 'absolute top-4 right-4',
    'bottom-right': 'absolute bottom-4 right-4',
    'bottom-left': 'absolute bottom-4 left-4',
    'center': 'mx-auto'
  };

  // Використовуємо онлайн QR генератор
  const qrSize = size === 'sm' ? '100x100' : size === 'md' ? '150x150' : size === 'lg' ? '200x200' : '300x300';
  const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=${qrSize}&data=${encodeURIComponent(url)}`;

  return (
    <div className={`${positionClasses[position]} ${className} z-10`}>
      <div className="bg-white/90 backdrop-blur-sm rounded-lg p-2 shadow-lg">
        <img 
          src={qrUrl} 
          alt="QR Code" 
          className={`${sizeClasses[size]} rounded`}
        />
        {showText && (
          <p className="text-xs text-gray-700 text-center mt-1 max-w-24">
            Демо
          </p>
        )}
      </div>
    </div>
  );
};

// Preset для презентації
export const PresentationQR: React.FC<Partial<QRCodeProps>> = (props) => (
  <QRCode 
    position="bottom-right"
    size="md"
    showText={true}
    {...props}
  />
);