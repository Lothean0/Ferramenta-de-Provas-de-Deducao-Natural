import { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/PropositionLogicBody.css';

import Warning from './Warning';

function PropositionLogicBody() {
    const [collapsed, setCollapsed] = useState(false);
    const [proofSteps, setProofSteps] = useState([]);

    const [screen, setScreen] = useState(0)
    const [expression, setExpression] = useState('')
    const [warning, setWarning] = useState('');


    const toggleNode = (nodeId) => {
        setCollapsed(prev => ({
            ...prev,
            [nodeId]: !prev[nodeId]
        }));
    };

    const nextScreen = () => {
        setScreen((prevScreen) => (prevScreen === 0 ? 1 : 0)); 
    };

    const renderTree = (nodes) => {
        if (!nodes || nodes.length === 0) return null;

        return (
            <div className="tree-level">
                {nodes.map((node, index) => {
                    const isCollapsed = collapsed[node.id];
                    const hasChildren = node.child && node.child.length > 0;
                    return (
                        <div key={index} className="tree-node">
                            <button className="node-label" onClick={() => toggleNode(node.id)}>
                              {isCollapsed ? '▶ ' : '▼ '} {node.id}: {node.name}
                            </button>

                            {!isCollapsed && hasChildren && <div className="line"></div>}

                            {!isCollapsed && renderTree(node.child)}
                        </div>
                    );
                })}
            </div>
        );
    };

    // Tree builder logic
    const createTreeCategoriesByParent = (categories, parentId = "") => {
      const siblings = [];
  
      categories.forEach(category => {
          if (category.parentId === parentId) {
              const children = createTreeCategoriesByParent(categories, category.id);
              category.child = children;
              siblings.push(category);
          }
      });
  
      return siblings;
    };
    
    const fetchData = () => {
        axios
            .get("/api/result", {
                params: {
                    expression: expression,
                    rule: "implication_introduction",
                    knowledge_base: [], 
                    id: 1, 
                    child: [],
                },
            })
            .then((response) => {
                console.log("API Response\n", response.data);

                const flatData = response.data.map((item, index) => ({
                    ...item,
                    id: index + 1,
                }));

                const treeData = createTreeCategoriesByParent(flatData);
                setProofSteps(treeData);
            })
            .catch((error) => {
                console.log(error)
                    if (error.response.status === 501 || error.response.status === 502) {
                        const message = `⚠️ Error: ${error.response.data.details}`;
                        setWarning(message)
                    } else {
                        console.error("Error fetching data:", error);
                    }
                });
    };


    return (
        <>
            <div className='main-container'>
                {screen === 0 ? (
                    // <FullTree/> 
                    <>  
                        <input
                            type="text"
                            value={expression}
                            onChange={(e) => setExpression(e.target.value)}
                            placeholder='Enter your expression'
                            className='expression-input'
                        />
                        <button className='fetch-data-bttn' onClick={fetchData}>Fetch Data</button>
                        <div className="render-tree-container">{renderTree(proofSteps)}</div>
                    </>
                ) : screen === 1 ? (
                    // <CurrentTree/> 
                    <h1>Hello world_4</h1>
                ) : null}
            </div>

            {/*
            <div className={`left-side-bar ${collapsed ? 'collapsed' : ''}`}>
                {screen === 0 ? (
                    <h1>Hello world_1</h1>
                ) : screen === 1 ? (
                    <h1>Hello world_2</h1>
                ) : null}
            </div>
            */}

            {warning && (
                <Warning 
                    message={warning} 
                    onClose={() => setWarning('')} 
                    autoDismiss={true} 
                    duration={2000}
                />
            )}


        </>
    );
}

export default PropositionLogicBody;
