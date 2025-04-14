import { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/PropositionLogicBody.css';

function PropositionLogicBody() {
    const [collapsed, setCollapsed] = useState({});
    const [proofSteps, setProofSteps] = useState([]);

    const toggleNode = (nodeId) => {
        setCollapsed(prev => ({
            ...prev,
            [nodeId]: !prev[nodeId]
        }));
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
  

    // Fetch data on component mount
    useEffect(() => {
      axios.get("http://127.0.0.1:3000/api/rule_result")
      .then(response => {

        console.log('API RESPONDE\n', response.data)

        const flatData = response.data.map((item, index) => ({
          ...item,
          id: index + 1 
        }));

        const treeData = createTreeCategoriesByParent(flatData);
        setProofSteps(treeData);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
    }, []);

    return (
        <div className="proofbox">
            {renderTree(proofSteps)}
        </div>
    );
}

export default PropositionLogicBody;
