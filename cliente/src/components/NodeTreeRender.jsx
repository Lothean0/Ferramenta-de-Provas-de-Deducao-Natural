import React from 'react';
import '../styles/NodeTreeRender.css';


// first try
/*
function NodeTreeRender({ node, toggleNode, renderTree, selectedNodeId, setSelectedNodeId }) {
    const hasChildren = node.child && node.child.length > 0;

    return (
        <div className="tree-node">
            <button
                className={`node-label ${selectedNodeId === node.id ? 'selected' : ''}`}
                onClick={() => {
                    toggleNode(node.id);
                    setSelectedNodeId(node.id);
                }}
            > {node.id} : {node.name}
            </button>


            <div className="line"></div>

            {renderTree(node.child)}
        </div>
    );
}
*/


function NodeTreeRender({ node, renderTree, selectedNodeId, setSelectedNodeId }) {
    const hasChildren = node.child && node.child.length > 0;
    console.log(node)
    return (
        <div className="tree-node-wrapper">
            <div className="tree-node">
                <button
                    className={`node-label ${selectedNodeId === node.id ? 'selected' : ''}`}
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

                {renderTree(node.child)}

            </div>
        </div>
    );
}


export default NodeTreeRender;
