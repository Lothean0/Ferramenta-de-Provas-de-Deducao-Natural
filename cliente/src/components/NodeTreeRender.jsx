import React from 'react';
import '../styles/NodeTreeRender.css';


function NodeTreeRender({ node, renderTree, selectedNodeId, setSelectedNodeId }) {
    const hasChildren = node.child && node.child.length > 0;
    const hasNoneChild = hasChildren && node.child.some(child => child.name === "None");

    return (
        <div className="tree-node-wrapper">
            <div className="tree-node">
                <button
                    className={`node-label ${selectedNodeId === node.id ? 'selected' : ''}`}
                    style={{
                        backgroundColor: hasNoneChild ? '#ffcdd2' : '#32de2f71'
                    }}
                    onClick={() => {
                        setSelectedNodeId(node.id);
                    }}
                ><span style={{ color: 'black' }}>{node.name}</span>
                </button>

                <div className="line"/>
                {/*    
                    <span style={{ color: 'black', position: 'relative', top: '10px', marginLeft: '50px' }}>{node.rule}</span>
                </div>
                */}

                {renderTree(node.child?.filter(child => child.name !== "None"))}

            </div>
        </div>
    );
}


export default NodeTreeRender;
