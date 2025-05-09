import { useState, useEffect, useRef, useMemo } from 'react';
import axios from 'axios';
import '../styles/PropositionLogicBody.css';
import { FiCheck } from "react-icons/fi";
import { Rnd } from 'react-rnd';

import landscape1 from '../assets/img/landscape-1.png';
import ImageWithTooltip from './ImageWithTooltip';


import NodeTreeRender from './NodeTreeRender';
import Warning from './Warning';
import ActionButton from './ActionButton';
import UploadArea from './UploadArea';
import SelectedNodeDetails from './SelectedNodeDetails';

import { translations } from '../utils/translations';
import { ruleOptions } from '../utils/ruleOptions';
import SegmentedControl from './SegmentedControl';

function PropositionLogicBody() {
    const [language, setLanguage] = useState('PT');
    const [activeInput, setActiveInput] = useState(null);
    const expressionInputRef = useRef(null);
    const knowledgebaseInputRef = useRef(null);

    const [tree, setTree] = useState([]);
    const [screen, setScreen] = useState(1);
    const [expressionInput, setExpressionInput] = useState('');
    const [ruleInput, setRuleInput] = useState('');
    const [auxiliarInput, setAuxiliarInput] = useState('');
    const [knowledgebaseInput, setKnowledgebaseInput] = useState('');
    const [knowledgebaseArray, setKnowledgebaseArray] = useState([]);
    const [selectedNodeId, setSelectedNodeId] = useState(1);
    const [warning, setWarning] = useState('');
    const [showUploadArea, setShowUploadArea] = useState(false);
    const [uploadedFileName, setUploadedFileName] = useState('');

    const [showRnd, setShowRnd] = useState(false);
    useEffect(() => {
        const timeout = setTimeout(() => setShowRnd(true), 100);
        return () => clearTimeout(timeout);
    }, []);


    const t = useMemo(() => (key) => translations[language][key] || key);


    useEffect(() => {
        resetData("/api/reset");
    }, []);
    

    const fetchData = (url) => {
        const selectedNode = findNodeById(tree, selectedNodeId);
        const nodeexpression = selectedNode?.name || expressionInput;
        const knowledgeBase = Object.entries(selectedNode?.knowledge_base || knowledgebaseArray);
        const uuid = selectedNode?.uuid || 0;

        axios.post(url, {
            uuid: uuid,
            expression: nodeexpression,
            rule: ruleInput,
            knowledge_base: [...knowledgeBase],
            id: selectedNodeId,
            child: [],
            auxiliar_formula: auxiliarInput,
            lambda: ""
        }, {
            headers: { 'Content-Type': 'application/json' }
        })
        .then((response) => {
            console.log(response)
            setKnowledgebaseArray([]);
            setAuxiliarInput('');
            const flatData = response.data.map((item, index) => ({
                ...item,
                id: index + 1,
            }));
            const treeData = createTreeCategoriesByParent(flatData);
            console.log(treeData)
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
                setKnowledgebaseInput('')
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
                console.log(res.data.fileName)
                const parsed = JSON.parse(res.data.filename);
                parsed.tree.forEach(node => {
                    if (node.name) {
                        node.name = node.name.replace('âˆ¨', '∨');
                        node.name = node.name.replace('âˆ§', '∧');
                        node.name = node.name.replace('âŸº', '⟺')
                    }
                });   
                console.log(parsed)
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
            if (node.id === id) {
                console.log("this is the node.id", node.id)
                if (node.name) {
                    node.name = node.name.replace('âˆ¨', '∨')
                                         .replace('âˆ§', '∧')
                                         .replace('âŸº', '⟺');
                }
                return node;
            }
            if (node.child) {
                const result = findNodeById(node.child, id);
                console.log("this is the result.id", result)
                if (result) {
                    if (result.name) {
                        result.name = result.name.replace('âˆ¨', '∨')
                                                 .replace('âˆ§', '∧')
                                                 .replace('âŸº', '⟺');
                    }
                return result;
                }
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


    const handleLanguageToggle = (selectedLanguage) => {
        setLanguage(selectedLanguage);
    };

    const appendToActiveInput = (value) => {
        const inputMap = {
            expression: [setExpressionInput, expressionInputRef],
            knowledgebase: [setKnowledgebaseInput, knowledgebaseInputRef]
        };
    
        const [setInput, inputRef] = inputMap[activeInput] || [];
    
        if (setInput && inputRef) {
            setInput(prev => {
                const newValue = prev + value;
                setTimeout(() => {
                    if (inputRef.current) {
                        inputRef.current.focus();
                        const len = inputRef.current.value.length;
                        inputRef.current.setSelectionRange(len, len);
                    }
                }, 0);
                return newValue;
            });
        }
    };
    
    
    
    
    

    return (
        <>
            <div className='main-container'>

                <SegmentedControl
                    onChange={handleLanguageToggle}
                />


                {screen === 0 ? (
                    <>
                        {showRnd && (
                            <Rnd
                                default={{
                                    x: window.innerWidth - (window.innerWidth <= 844 ? 210 : 310),
                                    y: 10,
                                    width: 300,
                                    height: window.innerHeight-20,
                                }}
                                minWidth={200}
                                maxWidth={350}
                                disableDragging
                                enableResizing={{
                                    left: true,
                                    right: false,
                                    top: false,
                                    bottom: false,
                                    topLeft: false,
                                    topRight: false,
                                    bottomLeft: false,
                                    bottomRight: false,
                                }}
                                resizeHandleStyles={{
                                    left: {
                                    left: '-6px',
                                    top: '50%',
                                    transform: 'translateY(-50%)',
                                    width: '12px',
                                    height: '50px',
                                    background: '#1a1a1a',
                                    cursor: 'ew-resize',
                                    borderRadius: '4px'
                                    }
                                }}
                                resizeHandleClasses={{
                                    left: 'resize-handle-left'
                                }}
                                className="general-information-container"
                                >
                                {/*
                                {selectedNodeId && (() => {
                                    const selectedNode = findNodeById(tree, selectedNodeId);
                                    console.log(selectedNode.id)
                                    return (
                                        <SelectedNodeDetails 
                                            node={selectedNode} 
                                            language={language} 
                                            translations={t}
                                            fallbackArray={knowledgebaseArray}
                                        />
                                    );
                                })()}
                                */}
                                {selectedNode && 
                                    <SelectedNodeDetails 
                                        node={selectedNode} 
                                        language={language} 
                                        translations={t}
                                        fallbackArray={knowledgebaseArray}
                                    />   
                                }
                            </Rnd>
                        )}

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

                        {showRnd && (
                            <Rnd
                                default={{
                                    x: window.innerWidth - (window.innerWidth <= 844 ? 210 : 310),
                                    y: 10,
                                    width: 300,
                                    height: window.innerHeight-20,
                                }}
                                minWidth={200}
                                maxWidth={350}
                                disableDragging
                                enableResizing={{
                                    left: true,
                                    right: false,
                                    top: false,
                                    bottom: false,
                                    topLeft: false,
                                    topRight: false,
                                    bottomLeft: false,
                                    bottomRight: false,
                                }}
                                resizeHandleStyles={{
                                    left: {
                                    left: '-6px',
                                    top: '50%',
                                    transform: 'translateY(-50%)',
                                    width: '12px',
                                    height: '50px',
                                    background: '#1a1a1a',
                                    cursor: 'ew-resize',
                                    borderRadius: '4px'
                                    }
                                }}
                                resizeHandleClasses={{
                                    left: 'resize-handle-left'
                                }}
                                className="general-information-container"
                                >
                                {/* adicionar findNodeById(nodeId, ...) */}
                                {selectedNode && 
                                    <SelectedNodeDetails 
                                        node={selectedNode} 
                                        language={language} 
                                        translations={t}
                                        fallbackArray={knowledgebaseArray}
                                    />
                                    
                                }
                            </Rnd>
                        )}

                        <div className='operators-bttn'>
                            <button 
                                aria-label='Insert implication symbol to input'
                                onClick={() =>  appendToActiveInput('->')}>{'->'}
                            </button>
                            <button 
                                aria-label='Insert conjunction symbol to input'
                                onClick={() =>  appendToActiveInput('∧')}>{'∧'}
                            </button>
                            <button 
                                aria-label='Insert disjunction symbol to input'
                                onClick={() =>  appendToActiveInput('∨')}>{'∨'}
                            </button>
                            <button 
                                aria-label='Insert equivalence symbol to input'
                                onClick={() =>  appendToActiveInput('⟺')}>{'⟺'}
                            </button>
                            <button 
                                aria-label='Insert negation symbol to input'
                                onClick={() =>  appendToActiveInput('~')}>{'~'}
                            </button>
                        </div>

                        <div className='knowledgebase-container'>
                            <input
                                ref={knowledgebaseInputRef}
                                type="text"
                                value={knowledgebaseInput}
                                onChange={(e) => setKnowledgebaseInput(e.target.value)}
                                onFocus={() => setActiveInput('knowledgebase')}
                                placeholder={t("knowledgePlaceholder")}
                                className='knowledgebase-input'
                            />
                            <button 
                                className='add-knowledgebase-bttn' 
                                aria-label='Add to knowledge base'
                                onClick={addToArray}
                            >
                                <FiCheck size={20} />
                            </button>
                        </div>
                        
                
                        <input
                            ref={expressionInputRef}
                            type="text"
                            value={expressionInput}
                            onChange={(e) => setExpressionInput(e.target.value)}
                            onFocus={() => setActiveInput('expression')}
                            placeholder={t("expressionPlaceholder")}
                            className='expression-input'
                        />

                        <div className='rule-container'>
                            <label className='rule-label'>
                                {t("selectRuleLabel")}
                                <select
                                    value={ruleInput}
                                    onChange={(e) => {
                                        console.log(e.target.value)
                                        setRuleInput(e.target.value)}
                                    }
                                    className='rule-input'
                                >
                                    <option value="">{t("selectRule")}</option>
                                    {Object.entries(ruleOptions).map(([key, label]) => (
                                    <option key={key} value={key}>
                                        {t(key)}
                                    </option>
                                    ))}
                                </select>
                            </label>

                            
                            {[
                                "Elim. Disjunção",
                                "Disjunction Elim.",
                                {/* missing other rules */}
                            ].includes(t(ruleInput)) && (
                                <>
                                    <input
                                    type="text"
                                    value={auxiliarInput}
                                    onChange={(e) => setAuxiliarInput(e.target.value)}
                                    placeholder="Auxiliar formula"
                                    className="auxiliar-formula-input"
                                    />
                                </>
                            )}
                        </div>


                        <div className="render-tree-container">
                            {renderSelectedNodeAndChildren()}
                        </div>
                    </>
                ) : (
                    <>
                        <div className='rules__container'
                        style={{ 
                            display: 'grid',
                            gridTemplateColumns: 'repeat(6, 1fr)',
                            gap: '2rem',
                            rowGap: '3.5rem',
                            marginLeft: '50px',
                            marginRight: '70px',
                            marginTop: '80px',

                            fontFamily: "'GochiHand', sans-serif",
                            position: 'absolute',
                            background: 'transparent'
                          }}
                        >
                            <ImageWithTooltip
                                src={landscape1} 
                                alt={t("axiom")}
                            />
                            <ImageWithTooltip
                                src={landscape1} 
                                alt={t("implication_introduction")}
                            />
                            <ImageWithTooltip
                                src={landscape1} 
                                alt={t("implication_elimination")}
                            />
                            <ImageWithTooltip
                                src={landscape1} 
                                alt={t("conjunction_introduction")}
                            />
                            <ImageWithTooltip
                                src={landscape1} 
                                alt={t("conjunction_elimination_1")}
                            />
                            <ImageWithTooltip
                                src={landscape1} 
                                alt={t("conjunction_elimination_2")}
                            />
                            <ImageWithTooltip
                                src={landscape1} 
                                alt={t("disjunction_introduction_1")}
                            />
                            <ImageWithTooltip
                                src={landscape1} 
                                alt={t("disjunction_introduction_2")}
                            />
                            <ImageWithTooltip
                                src={landscape1} 
                                alt={t("disjunction_elimination")}
                            />
                            <ImageWithTooltip
                                src={landscape1} 
                                alt={t("negation_introduction")}
                            />
                            <ImageWithTooltip
                                src={landscape1} 
                                alt={t("negation_elimination")}
                            />
                            <ImageWithTooltip
                                src={landscape1} 
                                alt={t("equivalence_introduction")}
                            />
                            <ImageWithTooltip
                                src={landscape1} 
                                alt={t("equivalence_elimination_1")}
                            />
                            <ImageWithTooltip
                                src={landscape1} 
                                alt={t("equivalence_elimination_2")}
                            />
                            <ImageWithTooltip
                                src={landscape1} 
                                alt={t("RAA")}
                            />
                            <ImageWithTooltip
                                src={landscape1} 
                                alt={t("absurd_elimination")}
                            />
                            
                        </div>
                    </>
                )}
            </div>

            
            <div className={`change-screen ${screen === 0 || screen === 1 ? 'on' : 'off'}`}>
                <button 
                    className='full-tree-screen-bttn' 
                    aria-label='Switch to full tree view'
                    onClick={() => setScreen(0)} 
                />
                <button 
                    className='small-tree-screen-bttn' 
                    aria-label='Switch to small tree view'
                    onClick={() => setScreen(1)} 
                    />
                <button 
                    className='help-screen-bttn' 
                    aria-label='Open help screen'
                    onClick={() => setScreen(2)}
                />
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