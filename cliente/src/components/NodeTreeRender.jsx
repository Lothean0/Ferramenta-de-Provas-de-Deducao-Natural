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

    return (
        <div className="tree-node-wrapper">
            <div className="tree-node">
                <button
                    className={`node-label ${selectedNodeId === node.id ? 'selected' : ''}`}
                    onClick={() => {
                        setSelectedNodeId(node.id);
                    }}
                > {node.id} : {node.name}
                </button>

                <div className="line"/>

                {renderTree(node.child)}

            </div>
        </div>
    );
}


export default NodeTreeRender;
