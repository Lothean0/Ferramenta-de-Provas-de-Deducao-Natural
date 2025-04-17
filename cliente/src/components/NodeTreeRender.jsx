import React from 'react';
import '../styles/NodeTreeRender.css';


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


            {hasChildren && <div className="line"></div>}

            {renderTree(node.child)}
        </div>
    );
}

export default NodeTreeRender;
