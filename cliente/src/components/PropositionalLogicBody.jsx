import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import '../styles/PropositionLogicBody.css';
import { FiCheck } from "react-icons/fi";


import NodeTreeRender from './NodeTreeRender';
import Warning from './Warning';

function PropositionLogicBody() {

    const [collapsed, setCollapsed] = useState(false)
    const [tree, setTree] = useState([]);
    const [screen, setScreen] = useState(1);
    const [expressionInput, setExpressionInput] = useState('');
    const [ruleInput, setRuleInput] = useState('');
    const [auxiliarInput, setAuxiliarInput] = useState('Y1')
    const [knowledgebaseInput, setKnowledgebaseInput] = useState('')
    const [knowledgebaseArray, setKnowledgebaseArray] = useState([]);

    const [selectedNodeId, setSelectedNodeId] = useState(1);
    const [warning, setWarning] = useState('');
    const [expressionvisibility, setExpressionVisibility] = useState(true);

    const [showUploadArea, setShowUploadArea] = useState(false);
    const [uploadedFileName, setUploadedFileName] = useState('');

    const ruleOptions = {
        axiom: "Axioma",
        implication_introduction: "Intro. Implicação",
        implication_elimination: "Elim. Implicação",
    };

    const toBeImplemented = {
        text1: "Intro. Conjunção",
        text1: "Elim. Conjunção_1",
        text1: "Elim. Conjunção_2",
        text1: "Intro. Disjunção_1",
        disjunction_introduction_2: "Introdução Disjunção_2",
        disjunction_eliminations: "Elim. Disjunção",
        negation_introduction: "Intro. Negação",
        ifAndOnlyIf_introduction: "Intro. Bicondicional",
        ifAndOnlyIf_eliminations_1: "Elim. Bicondicional_1",
        ifAndOnlyIf_eliminations_2: "Elim. Bicondicional_2",
    }

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

    const fetchData = (url) => {
        setExpressionVisibility(false);

        const selectedNode = findNodeById(tree, selectedNodeId);
        const nodeexpression = selectedNode?.name || expressionInput;
        const knowledgeBase = Object.entries(selectedNode?.knowledge_base || knowledgebaseArray);

        axios
            .post(url, {
                expression: nodeexpression,
                rule: ruleInput,
                knowledge_base: [...knowledgeBase],
                id: selectedNodeId,
                child: [],
                auxiliar_formula: auxiliarInput,
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then((response) => {
                setKnowledgebaseArray([])
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
                if (error.response?.status === 400 || error.response?.status === 422 || error.response?.status === 500) {
                    const message = `⚠️ Error: ${error.response.data.error}`;
                    setWarning(message)
                } else {
                    console.log("Error fetching data: ", error)
                }
            });
    };

    const resetData = (url) => {
        axios
            .post(url)
            .then((response) => {
                console.log("API Response\n", response.data);
                setExpressionVisibility(true);

                const flatData = response.data.map((item, index) => ({
                    ...item,
                    id: index + 1,
                }));

                const treeData = createTreeCategoriesByParent(flatData);
                setTree(treeData);
                setRuleInput('');
                setExpressionInput('');
                setKnowledgebaseArray([])
            })
            .catch((error) => {
                console.error("API Error\n", error);
            });
    };

    const saveData = (url) => {
        axios
            .post(url, {
                tree
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then((response) => {
                console.log("API Response\n", response.data)

                const fileNumber = response.data.number;
                const fileName = `tree-data-${fileNumber}.json`

                const jsonString = JSON.stringify({tree}, null, 2);
                const blob = new Blob([jsonString], {type: 'application/json'});
                const urlBlob = URL.createObjectURL(blob);
                const link = document.createElement('a')
                
                link.href = urlBlob;
                link.download = fileName;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(urlBlob);
            })
            .catch((error) => {
                console.error("API Error\n", error)
            })
    }

    const handleFileDrop = (e) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        axios.post('api/file', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
        .then((res) => {
            setUploadedFileName(res.data.filename || 'Upload successful');
            setShowUploadArea(false);

            try {
                // Step 1: Parse first layer
                const parsed = JSON.parse(res.data.filename);
    
                // Step 2: Get tree data
                const uploadedTree = parsed.tree;
    
                setTree(uploadedTree);
                setSelectedNodeId(uploadedTree[0]?.id || 1); 
                setUploadedFileName('')
            } catch (err) {
                console.error("Parsing uploaded file failed:", err);
                setWarning("⚠️ Invalid file format.");
            }
        })
        .catch((err) => {
            console.error("File upload error:", err);
            setUploadedFileName('Upload failed');
        });
    };

    const handleDragOver = (e) => {
        e.preventDefault();
    };

    const renderSelectedNodeAndChildren = () => {
        if (!selectedNodeId) return <p>Selecione um no.</p>;

        const selectedNode = findNodeById(tree, selectedNodeId);

        if (!selectedNode) return <></>;

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
                                    renderTree={() => null} 
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

    const addToArray = () => {
        if (knowledgebaseInput.trim() !== '') {
            const trimmedInput = knowledgebaseInput.trim();
            const newArray = [...knowledgebaseArray, trimmedInput];
            console.log(newArray);
            setKnowledgebaseArray(newArray);
            setKnowledgebaseInput('');
        }
    };
    

    return (
        <>
            <div className='main-container'>
                <button className='reset-bttn' onClick={() => resetData("/api/reset")}>Reset</button>
                <button className={`add-node-bttn ${expressionvisibility ? 'show' : 'hidden'}`} onClick={() => fetchData("/api/node")}>Add Node</button>
                <button className='apply-rule-bttn' onClick={() => fetchData("/api/rules")}>Apply Rule</button>            

                <button className='upload-file-bttn' onClick={() => setShowUploadArea(!showUploadArea)}>
                    {showUploadArea ? "Close Upload" : "Upload File"}
                </button>

                {showUploadArea && (
                    <div 
                        className="drop-area" 
                        onDrop={handleFileDrop} 
                        onDragOver={handleDragOver}
                    >
                        {uploadedFileName ? (
                            <p>{uploadedFileName}</p>
                        ) : (
                            <p>Drag and drop a file here</p>
                        )}
                    </div>
                )}

                <button className='save-bttn' onClick={() => saveData("/api/save")}>Downlad</button>

                {screen === 0 ? (
                    <>
                        <div className="render-tree-container">{renderTree(tree)}</div>
                    </>
                ) : (
                    <>        
                        
                        <input
                            type="text"
                            value={expressionInput}
                            onChange={(e) => setExpressionInput(e.target.value)}
                            placeholder='p0 -> (p1->(p2 -> (p3 ->p4)))'
                            className={`expression-input ${expressionvisibility ? 'show' : 'hidden'}`}
                        />
                        

                        <div className='knowledgebase-container'>
                            <input
                                type="text"
                                value={knowledgebaseInput}
                                onChange={(e) => setKnowledgebaseInput(e.target.value)}
                                placeholder='p0'
                                className='knowledgebase-input'
                            />
                            <button className='add-knowledgebase-bttn' onClick={addToArray}>
                                <FiCheck size={20} />
                            </button>
                        </div>

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
                        <div className="render-tree-container">
                            {renderSelectedNodeAndChildren()}
                        </div>
                    </>
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
                    duration={10000}
                />
            )}
        </>
    );
}

export default PropositionLogicBody;
