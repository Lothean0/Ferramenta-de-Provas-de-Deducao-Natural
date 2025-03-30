import { useState } from 'react';
import axios from 'axios';
import '../styles/CoqBody.css';
import { BsGear, BsCaretRightSquare, BsArrowDown, BsXLg } from "react-icons/bs";

function CoqBody() {
    const [lines, setLines] = useState(
        Array.from({ length: 17 }, (_, i) => ({ id: i + 1, text: '' }))
    );
    const [currentLineId, setCurrentLineId] = useState(null);

    const handleLineChange = (id, newText) => {
        setLines(lines.map(line => (line.id === id ? { ...line, text: newText } : line)));
    };

    const handleKeyDown = (id, event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            const nextId = id + 1;
            const existingLine = lines.find(line => line.id === nextId);

            if (!existingLine) {
                setLines(prevLines => [...prevLines, { id: nextId, text: '' }]);
            }

            setTimeout(() => {
                const nextInput = document.getElementById(`input-${nextId}`);
                if (nextInput) {
                    nextInput.focus();
                }
            }, 0);
        } else if (event.key === 'ArrowDown') {
            event.preventDefault();
            const nextId = id + 1;
            const nextInput = document.getElementById(`input-${nextId}`);
            if (nextInput) {
                nextInput.focus();
            }
        } else if (event.key === 'ArrowUp') {
            event.preventDefault();
            const prevId = id - 1;
            const prevInput = document.getElementById(`input-${prevId}`);
            if (prevInput) {
                prevInput.focus();
            }
        }
    };

    const sendToBackend = async (currentId) => {
        if (currentId === null || currentId === 0) return;
    
        const currentLine = lines.find(line => line.id === currentId);
        if (!currentLine) return;
    
        try {
            const response = await axios.post('http://127.0.0.1:3000/api/checkExpression', {
                currentLineId: currentLine.id,
                text: currentLine.text
            });
            console.log('Response:', response.data);
        } catch (error) {
            console.error('Error sending data:', error);
        }
    };
    
    const handleDownArrow = () => {
        if (currentLineId < lines.length) {
            setCurrentLineId(currentLineId + 1);
            sendToBackend();
        }
    };

    const handleStop = () => {
        setCurrentLineId(-1);
    };

    return (
        <div className='propositional-logic-container'>
            <div className='navbar'>
                <button className='settings-button'>
                    <BsGear style={{ color: 'cyan' }} />
                </button>
                <button className='start-button' onClick={() => setCurrentLineId(0)}>
                    <BsCaretRightSquare style={{ color: 'cyan' }} />
                </button>
                <button className='down-arrow-button' onClick={handleDownArrow}>
                    <BsArrowDown style={{ color: 'cyan' }} />
                </button>
                <button className='stop-arrow-button' onClick={handleStop}>
                    <BsXLg style={{ color: 'cyan' }} />
                </button>
            </div>

            <div className='left-side'>
                {lines.map((line) => (
                    <div key={line.id} className='notebook-line'>
                        <span className='line-id'>{line.id}.</span>
                        <input
                            id={`input-${line.id}`}
                            type='text'
                            value={line.text}
                            onChange={(e) => handleLineChange(line.id, e.target.value)}
                            onKeyDown={(e) => handleKeyDown(line.id, e)}
                        />
                    </div>
                ))}
            </div>

            <div className='right-top-side'>
                {currentLineId !== 0 && currentLineId !== null && (
                    <div>
                        <strong>Line {currentLineId}:</strong> {lines.find(line => line.id === currentLineId)?.text}
                    </div>
                )}
            </div>
            <div className='right-bottom-side'></div>
        </div>
    );
}

export default CoqBody;
