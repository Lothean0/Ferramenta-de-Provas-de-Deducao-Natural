import React, { useState, useEffect } from 'react';
import { Rnd } from 'react-rnd';
import SelectedNodeDetails from './SelectedNodeDetails';

const ReactiveRnd = ({ selectedNode, language, t, knowledgebaseArray, showRnd, screen, flag }) => {

    const [position, setPosition] = useState({
        x: window.innerWidth - (window.innerWidth <= 844 ? 210 : 310),
        y: 10,
    });
    const [size, setSize] = useState({
        width: 300,
        height: window.innerHeight - 20,
    });

    const onDragStop = (e, d) => {
        setPosition({
        x: d.x,
        y: d.y,
        });
    };

    const onResizeStop = (e, direction, ref, delta, position) => {
        setSize({
        width: ref.offsetWidth,
        height: ref.offsetHeight,
        });
        setPosition(position);
    };

    useEffect(() => {
        setSize((prevSize) => ({
        ...prevSize,
        height: window.innerHeight - 20,
        }));
    }, [window.innerHeight]);

    return (
        (screen === 0 || screen === 1) && showRnd && (
        <Rnd
            position={position}
            size={size}
            onDragStop={onDragStop}
            onResizeStop={onResizeStop}
            minWidth={200}
            maxWidth={350}
            disableDragging={false}
            enableResizing={{
            left: true,
            right: false,
            top: false,
            bottom: false,
            topLeft: false,
            topRight: false,
            bottomLeft: false,
            bottomRight: false,
            }}
            resizeHandleStyles={{
            left: {
                left: '-6px',
                top: '50%',
                transform: 'translateY(-50%)',
                width: '12px',
                height: '50px',
                background: '#1a1a1a',
                cursor: 'ew-resize',
                borderRadius: '4px',
            },
            }}
            resizeHandleClasses={{
            left: 'resize-handle-left',
            }}
            className="general-information-container"
        >
            {selectedNode && (
            <SelectedNodeDetails
                node={selectedNode}
                language={language}
                translations={t}
                fallbackArray={knowledgebaseArray}
            />
            )}
        </Rnd>
        )
    );
};

export default ReactiveRnd;
