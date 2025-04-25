import { useState, useEffect, useRef, useMemo } from 'react';
import axios from 'axios';
import '../styles/PropositionLogicBody.css';
import { FiCheck } from "react-icons/fi";

import NodeTreeRender from './NodeTreeRender';
import Warning from './Warning';
import ActionButton from './ActionButton';
import UploadArea from './UploadArea';
import SelectedNodeDetails from './SelectedNodeDetails';

import { translations } from '../utils/translations';
import { ruleOptions } from '../utils/ruleOptions';

function PropositionLogicBody() {
    const [language, setLanguage] = useState('PT');
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

    const t = useMemo(() => (key) => translations[language][key] || key);


    
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

    const selectedNode = useMemo(() => findNodeById(tree, selectedNodeId), [tree, selectedNodeId]);


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
        if (!selectedNode) return <p>Selecione um no.</p>;

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
            return newLanguage;
        });
    };
    

    return (
        <>
            <div className='main-container'>

                <ActionButton
                            className='language-bttn'
                            onClick={handleLanguageToggle}
                            label={t("language")}
                />


                {screen === 0 ? (
                    <>
                        <div className="general-information-container">
                            {selectedNodeId && (() => {
                                const selectedNode = findNodeById(tree, selectedNodeId);
                                return (
                                    <SelectedNodeDetails 
                                        node={selectedNode} 
                                        language={language} 
                                        translations={t}
                                        fallbackArray={knowledgebaseArray}
                                    />
                                );
                            })()}
                        </div>

                        <div className="render-tree-container">{renderTree(tree)}</div>
                    </>
                ) : screen === 1 ? (
                    <>

                        <ActionButton
                            className='reset-bttn'
                            onClick={() => resetData("/api/reset")}
                            label={t("reset")}
                        />

                        <ActionButton 
                            className='add-node-bttn' 
                            onClick={() => fetchData("/api/node")} 
                            label={t("addNode")} 
                        />

                        <ActionButton 
                            className='apply-rule-bttn' 
                            onClick={() => fetchData("/api/rules")} 
                            label={t("applyRule")} 
                        />

                        <ActionButton 
                            className='upload-file-bttn' 
                            onClick={() => setShowUploadArea(!showUploadArea)} 
                            label={showUploadArea ? t("uploadClose") : t("uploadOpen")} 
                        />

                        <UploadArea
                            show={showUploadArea}
                            onDrop={handleFileDrop}
                            onDragOver={handleDragOver}
                            fileName={uploadedFileName}
                            message={t("dragDrop")}
                        />

                        <ActionButton 
                            className='save-bttn' 
                            onClick={() => saveData("/api/save")} 
                            label={t("download")} 
                        />

                        <div className="general-information-container">
                            {selectedNodeId && (() => {
                                const selectedNode = findNodeById(tree, selectedNodeId);
                                return (
                                    <SelectedNodeDetails 
                                        node={selectedNode} 
                                        language={language} 
                                        translations={t}
                                        fallbackArray={knowledgebaseArray}
                                    />
                                );
                            })()}
                        </div>
                        
                        <input
                            type="text"
                            value={expressionInput}
                            onChange={(e) => setExpressionInput(e.target.value)}
                            placeholder={t("expressionPlaceholder")}
                            className='expression-input'
                        />

                        <div className='knowledgebase-container'>
                            <input
                                type="text"
                                value={knowledgebaseInput}
                                onChange={(e) => setKnowledgebaseInput(e.target.value)}
                                placeholder={t("knowledgePlaceholder")}
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
                            <option value="">{t("selectRule")}</option>
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
                    <>
                    </>


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
