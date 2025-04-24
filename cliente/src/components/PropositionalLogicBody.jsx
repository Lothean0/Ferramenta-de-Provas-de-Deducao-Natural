import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import '../styles/PropositionLogicBody.css';
import { FiCheck } from "react-icons/fi";

import NodeTreeRender from './NodeTreeRender';
import Warning from './Warning';

function PropositionLogicBody() {
    const [language, setLanguage] = useState('PT');
    const translations = {
        EN: {
            reset: "Reset",
            addNode: "Add Node",
            applyRule: "Apply Rule",
            uploadOpen: "Open Upload",
            uploadClose: "Close Upload",
            download: "Download",
            selectRule: "Select a rule",
            dragDrop: "Drag and drop a file here",
            expressionPlaceholder: "Enter expression: p0 -> (p1 -> p2)",
            knowledgePlaceholder: "Enter Gamma values: p1, p5",
            language: "EN"
        },
        PT: {
            reset: "Reiniciar",
            addNode: "Adicionar Nó",
            applyRule: "Aplicar Regra",
            uploadOpen: "Abrir Upload",
            uploadClose: "Fechar Upload",
            download: "Baixar",
            selectRule: "Selecione uma regra",
            dragDrop: "Arraste e solte um arquivo aqui",
            expressionPlaceholder: "Insira expressão: p0 -> (p1 -> p2)",
            knowledgePlaceholder: "Insira valores Gamma: p0, p5",
            language: "PT"
        }
    };

    const [tree, setTree] = useState([]);
    const [screen, setScreen] = useState(1);
    const [expressionInput, setExpressionInput] = useState('');
    const [ruleInput, setRuleInput] = useState('');
    const [auxiliarInput, setAuxiliarInput] = useState('Y1');
    const [knowledgebaseInput, setKnowledgebaseInput] = useState('');
    const [knowledgebaseArray, setKnowledgebaseArray] = useState([]);
    const [selectedNodeId, setSelectedNodeId] = useState(1);
    const [warning, setWarning] = useState('');
    const [showUploadArea, setShowUploadArea] = useState(false);
    const [uploadedFileName, setUploadedFileName] = useState('');

    const ruleOptions = {
        axiom: "Axioma",
        implication_introduction: "Intro. Implicação",
        implication_elimination: "Elim. Implicação",
    };

    
    useEffect(() => {
        resetData("/api/reset");
    }, []);
    

    const fetchData = (url) => {
        const selectedNode = findNodeById(tree, selectedNodeId);
        const nodeexpression = selectedNode?.name || expressionInput;
        const knowledgeBase = Object.entries(selectedNode?.knowledge_base || knowledgebaseArray);

        axios.post(url, {
            expression: nodeexpression,
            rule: ruleInput,
            knowledge_base: [...knowledgeBase],
            id: selectedNodeId,
            child: [],
            auxiliar_formula: auxiliarInput,
        }, {
            headers: { 'Content-Type': 'application/json' }
        })
        .then((response) => {
            console.log(response)
            setKnowledgebaseArray([]);
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
            if (error.response?.status >= 400 && error.response?.status < 600) {
                setWarning(`⚠️ Error: ${error.response.data.error}`);
            } else {
                console.error("Error fetching data:", error);
            }
        });
    };

    const resetData = (url) => {
        axios.post(url)
            .then((response) => {
                const flatData = response.data.map((item, index) => ({
                    ...item,
                    id: index + 1,
                }));
                const treeData = createTreeCategoriesByParent(flatData);
                setTree(treeData);
                setSelectedNodeId(treeData[0]?.id || 1);
                setRuleInput('');
                setExpressionInput('');
                setKnowledgebaseArray([]);
                setScreen(1);
            })
            .catch((error) => console.error("API Error:", error));
    };

    const saveData = (url) => {
        axios.post(url, { tree }, {
            headers: { 'Content-Type': 'application/json' }
        })
        .then((response) => {
            const fileNumber = response.data.number;
            const fileName = `tree-data-${fileNumber}.json`;
            const jsonString = JSON.stringify({ tree }, null, 2);
            const blob = new Blob([jsonString], { type: 'application/json' });
            const urlBlob = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = urlBlob;
            link.download = fileName;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(urlBlob);
        })
        .catch((error) => console.error("API Error:", error));
    };

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
                const parsed = JSON.parse(res.data.filename);
                const uploadedTree = parsed.tree;
                setTree(uploadedTree);
                setSelectedNodeId(uploadedTree[0]?.id || 1);
                setUploadedFileName('');
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

    const handleDragOver = (e) => e.preventDefault();

    const addToArray = () => {
        if (knowledgebaseInput.trim() !== '') {
            const newArray = [...knowledgebaseArray, knowledgebaseInput.trim()];
            setKnowledgebaseArray(newArray);
            setKnowledgebaseInput('');
        }
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

    const renderTree = (nodes) => {
        if (!nodes || nodes.length === 0) return null;
        return (
            <div className="tree-level">
                {nodes.map((node, index) => (
                    <NodeTreeRender
                        key={index}
                        node={node}
                        renderTree={renderTree}
                        selectedNodeId={selectedNodeId}
                        setSelectedNodeId={setSelectedNodeId}
                    />
                ))}
            </div>
        );
    };

    const renderSelectedNodeAndChildren = () => {
        if (!selectedNodeId) return <p>Selecione um no.</p>;
        const selectedNode = findNodeById(tree, selectedNodeId);
        if (!selectedNode) return <></>;

        return (
            <div className="tree-level">
                <NodeTreeRender
                    node={selectedNode}
                    renderTree={(nodes) => (
                        <div className="tree-level">
                            {nodes.map((node, index) => (
                                <NodeTreeRender
                                    key={index}
                                    node={node}
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

    const handleLanguageToggle = () => {
        setLanguage(prev => {
            const newLanguage = prev === 'EN' ? 'PT' : 'EN';
            console.log('Toggled to:', newLanguage);  // Check language toggling
            return newLanguage;
        });
    };

    return (
        <>
            <div className='main-container'>
                <button className='language-bttn' onClick={handleLanguageToggle }>
                    {translations[language].language}
                </button>


                <button className='reset-bttn' onClick={() => resetData("/api/reset")}>
                    {translations[language].reset}
                </button>

                <button className='add-node-bttn' onClick={() => fetchData("/api/node")}>
                    {translations[language].addNode}
                </button>

                <button className='apply-rule-bttn' onClick={() => fetchData("/api/rules")}>
                    {translations[language].applyRule}
                </button>

                <button className='upload-file-bttn' onClick={() => setShowUploadArea(!showUploadArea)}>
                    {showUploadArea ? translations[language].uploadClose : translations[language].uploadOpen}
                </button>

                {showUploadArea && (
                    <div className="drop-area" onDrop={handleFileDrop} onDragOver={handleDragOver}>
                        <p>{uploadedFileName || translations[language].dragDrop}</p>
                    </div>
                )}

                <button className='save-bttn' onClick={() => saveData("/api/save")}>
                    {translations[language].download}
                </button>

                <div className='general-information-container'>
                    {(() => {
                        const selectedNode = findNodeById(tree, selectedNodeId);
                        const nodeId = selectedNode?.id || null
                        const nodeName = selectedNode?.name || null
                        const nodeParentId = selectedNode?.parentId || null
                        const nodeKnowledgeBase = Object.entries(selectedNode?.knowledge_base || knowledgebaseArray);
                        return selectedNode ? (
                            <>
                                <p><strong>ID:</strong> {nodeId}</p>
                                <p><strong>Name:</strong> {nodeName}</p>
                                <p><strong>Parent ID:</strong>{nodeParentId}</p>
                                <p><strong>Knowledge Base:</strong></p>
                                <ul style={{ listStyleType: 'none', paddingLeft: 50 }}>
                                    {nodeKnowledgeBase.map(([key, value], index) => (
                                        <li key={index}>
                                        <strong>{key}:</strong> {value}
                                        </li>
                                    ))}
                                </ul>
                            </>
                        ) : (
                            null
                        );
                    })()}
                </div>

                {screen === 0 ? (
                    <div className="render-tree-container">{renderTree(tree)}</div>
                ) : screen === 1 ? (
                    <>
                        
                        <input
                            type="text"
                            value={expressionInput}
                            onChange={(e) => setExpressionInput(e.target.value)}
                            placeholder={translations[language].expressionPlaceholder}
                            className='expression-input'
                        />

                        <div className='knowledgebase-container'>
                            <input
                                type="text"
                                value={knowledgebaseInput}
                                onChange={(e) => setKnowledgebaseInput(e.target.value)}
                                placeholder={translations[language].knowledgePlaceholder}
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
                            <option value="">{translations[language].selectRule}</option>
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
                ) : (
                    null
                )}
            </div>

            <div className='change-screen'>
                <button className='screen-0-bttn' onClick={() => setScreen(0)} />
                <button className='screen-1-bttn' onClick={() => setScreen(1)} />
                <button className='screen-2-bttn' onClick={() => setScreen(2)} />
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
