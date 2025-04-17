import { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/PropositionLogicBody.css';

import NodeTreeRender from './NodeTreeRender';
import Warning from './Warning';

function PropositionLogicBody() {
    const [collapsed, setCollapsed] = useState(false);
    const [tree, setTree] = useState([]);

    const [screen, setScreen] = useState(0)
    const [expressionInput, setExpressionInput] = useState('')
    const [ruleInput, setRuleInput] = useState('')

    const [selectedNodeId, setSelectedNodeId] = useState(1);
    const [warning, setWarning] = useState('');

    const [expressionvisibility, setExpressionVisibility] = useState(true)

    const ruleOptions = {
        implication_introduction: "Introdução da Implicação",
        implication_eliminations: "Eliminação da Implicação",
        axiom_rule: "Axioma",
        conjunction_introduction: "Introdução da Conjunção",
        conjunction_eliminations_1: "Eliminação da Conjunção_1",
        conjunction_eliminations_2: "Eliminação da Conjunção_2",
        disjunction_introduction_1: "Introdução da Disjunção_1",
        disjunction_introduction_2: "Introdução da Disjunção_2",
        disjunction_eliminations: "Eliminação da Disjunção",
        negation_introduction: "Introdução da Negação",
        ifAndOnlyIf_introduction: "Introdução da Bicondicional",
        ifAndOnlyIf_eliminations_1: "Eliminação da Bicondicional_1",
        ifAndOnlyIf_eliminations_2: "Eliminação da Bicondicional_2",
    };

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
                {nodes.map((node, index) => (
                    <NodeTreeRender
                        key={index}
                        node={node}
                        toggleNode={toggleNode}
                        renderTree={renderTree}
                        selectedNodeId={selectedNodeId}
                        setSelectedNodeId={setSelectedNodeId}
                    />
                ))}
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

    // Helper to find node by ID
    const findNodeById = (nodes, id) => {
        for (const node of nodes) {
            if (node.id === id) return node;
            if (node.child) {
                const result = findNodeById(node.child, id);
                if (result) return result;
            }
        }
        return null;
    };

    const fetchData = () => {

        setExpressionVisibility(false)

        const selectedNode = findNodeById(tree, selectedNodeId);
        const nodeexpression = selectedNode?.name || expressionInput

        const knowledgeBase = selectedNode?.knowledge_base || [];

        axios
            .get("/api/result", {
                params: {
                    expression: nodeexpression,
                    rule: ruleInput,
                    knowledge_base: knowledgeBase,
                    id: selectedNodeId,
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
                setTree(treeData);
                setRuleInput('');
                setExpressionInput('');
            })
            .catch((error) => {
                console.log(error);
                if (error.response?.status === 501 || error.response?.status === 502) {
                    const message = `⚠️ Error: ${error.response.data.details}`;
                    setWarning(message);
                } else if (error.response?.status === 401) {
                    const message = `⚠️ Error: ${error.response.data.error}`;
                    setWarning(message);
                } else {
                    console.error("Error fetching data:", error);
                }
            });
    };

    const renderSelectedNodeAndChildren = () => {
        if (!selectedNodeId) return <p>Selecione um nó.</p>;

        const selectedNode = findNodeById(tree, selectedNodeId);

        if (!selectedNode) return <p>Nó não encontrado.</p>;

        return (
            <div className="tree-level">
                <NodeTreeRender
                    node={selectedNode}
                    toggleNode={toggleNode}
                    renderTree={(nodes) => (
                        <div className="tree-level">
                            {nodes.map((node, index) => (
                                <NodeTreeRender
                                    key={index}
                                    node={node}
                                    toggleNode={toggleNode}
                                    renderTree={() => null} // Only direct children
                                    selectedNodeId={selectedNodeId}
                                    setSelectedNodeId={setSelectedNodeId}
                                />
                            ))}
                        </div>
                    )}
                    selectedNodeId={selectedNodeId}
                    setSelectedNodeId={setSelectedNodeId}
                />
            </div>
        );
    };

    return (
        <>
            <div className='main-container'>
                {screen === 0 ? (
                    <>
                        <input
                            type="text"
                            value={expressionInput}
                            onChange={(e) => setExpressionInput(e.target.value)}
                            placeholder='Enter your expression'
                            className={`expression-input ${expressionvisibility ? 'show' : 'hidden'}`}
                            />

                        <select
                            value={ruleInput}
                            onChange={(e) => setRuleInput(e.target.value)}
                            className='rule-input'
                        >
                            <option value="">Select a rule</option>
                            {Object.entries(ruleOptions).map(([key, label]) => (
                                <option key={key} value={key}>
                                    {label}
                                </option>
                            ))}
                        </select>

                        <button className='fetch-data-bttn' onClick={fetchData}>Fetch Data</button>
                        <div className="render-tree-container">{renderTree(tree)}</div>
                    </>
                ) : (
                    <div className="render-tree-container">
                        {renderSelectedNodeAndChildren()}
                    </div>
                )}
            </div>

            <div className='change-screen'>
                <button className='screen-1-bttn' onClick={() => setScreen(0)} />
                <button className='screen-2-bttn' onClick={() => setScreen(1)} />
            </div>

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
