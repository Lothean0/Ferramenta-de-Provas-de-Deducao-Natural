import React from 'react';

const UploadArea = ({ show, onDrop, onDragOver, fileName, message }) => {
    if (!show) return null;
    return (
        <div className="drop-area" onDrop={onDrop} onDragOver={onDragOver}>
            <p>{fileName || message}</p>
        </div>
    );
};

export default UploadArea;
