import React, { useState } from 'react';

const ImageWithTooltip = ({ src, alt }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      style={
        { 
            position: 'relative', 
            display: 'inline-block', 
            overflow: 'hidden' ,
            transition: 'transform 0.3s ease',
            transform: isHovered ? 'scale(1.15)' : 'scale(1)',
            zIndex: isHovered ? 2: 1

        }
    }
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <img
        src={src}
        alt={alt}
        style={{
          width: '300px',
          height: 'auto',
          display: 'block',
          borderRadius: '8px',
        }}
      />
      {isHovered && (
        <div
          style={{
            position: 'absolute',
            bottom: '10px',
            left: '50%',
            transform: 'translateX(-50%)',
            backgroundColor: 'rgba(29, 146, 255, 0.75)',
            color: '#fff',
            padding: '5px 10px',
            borderRadius: '4px',
            whiteSpace: 'nowrap',
            fontSize: '14px',
            zIndex: 1,
          }}
        >
          {alt}
        </div>
      )}
    </div>
  );
};

export default ImageWithTooltip;
