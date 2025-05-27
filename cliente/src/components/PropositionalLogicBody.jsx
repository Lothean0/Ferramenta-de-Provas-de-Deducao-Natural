import { useState, useEffect, useRef, useMemo } from 'react';
import axios from 'axios';
import '../styles/PropositionLogicBody.css';
import { FiAlertOctagon, FiCheck } from "react-icons/fi";

import Info from './Info';
import NodeTreeRender from './NodeTreeRender';
import Warning from './Warning';
import ActionButton from './ActionButton';
import UploadArea from './UploadArea';

import { translations } from '../utils/translations';
import { ruleOptions } from '../utils/ruleOptions';
import SegmentedControl from './SegmentedControl';
import ReactiveRnd from './ReactiveRnd';

function PropositionLogicBody() {
    const [language, setLanguage] = useState('PT');
    const [activeInput, setActiveInput] = useState(null);
    const expressionInputRef = useRef(null);
    const knowledgebaseInputRef = useRef(null);
    const auxiliarInputRef = useRef(null);

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

    const [isHidden, setIsHidden] = useState(false);

    const [showTutorial, setShowTutorial] = useState(false);

    const [completedproof, setCompletedProof] = useState(true);

    function treeHasRule(nodes, rule) {
        for (const node of nodes) {
            if (node.rule === rule) return true;
            if (node.child && treeHasRule(node.child, rule)) return true;
        }
        return false;
    }

    useEffect(() => {
        const ruleToCheck = "{rule}";
        if (tree.length === 0 || treeHasRule(tree, ruleToCheck)) {
            setCompletedProof(false);
        } else {
            setCompletedProof(true);
        }
    }, [tree]);
    

    const SYMBOLS = [
        { symbol: '→', label: 'implication' },
        { symbol: '∧', label: 'conjunction' },
        { symbol: '∨', label: 'disjunction' },
        { symbol: '⟺', label: 'equivalence' },
        { symbol: '~', label: 'negation' },
        { symbol: '⊥', label: 'falsum' },
    ];

    const [showRnd, setShowRnd] = useState(false);
    useEffect(() => {
        const timeout = setTimeout(() => setShowRnd(true), 100);
        return () => clearTimeout(timeout);
    }, []);


    const t = useMemo(() => (key) => translations[language][key] || key);


    useEffect(() => {
        resetData("/api/reset");
    }, []);
    

    const fetchData = (url, kbArray) => {
        const selectedNode = findNodeById(tree, selectedNodeId);
        const nodeexpression = selectedNode?.name || expressionInput;
        const knowledgeBase = Object.entries(selectedNode?.knowledge_base || kbArray);
        const uuid = selectedNode?.uuid || 0;

        console.log(knowledgeBase)

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
            setIsHidden(true);
        })
        .catch((error) => {
            if (error.response?.status === 400 || error.response?.status === 422 || error.response?.status === 500 ) {
                setWarning(`⚠️ Error: ${error.response.data.details}`);
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
                setIsHidden(false)
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

    /*
    const charReplacements = {
        'â†’' : '→',
        'âˆ¨': '∨',
        'âˆ§': '∧',
        'âŸº': '⟺',
        'âŠ¥': '⊥'
    };

    const cleanName = (name) => {
        return name.replace(/â†’|âˆ¨|âˆ§|âŸº|âŠ¥/g, match => charReplacements[match] || match);
    };
    */


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
                /*
                parsed.tree.forEach(node => {
                    if (node.name) {
                        node.name = cleanName(node.name);
                    }
                });
                */   
                console.log(parsed)
                const uploadedTree = parsed.tree;
                setTree(uploadedTree);
                setSelectedNodeId(uploadedTree[0]?.id || 1);
                setUploadedFileName('');
                setIsHidden(true);
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
        if (knowledgebaseInput.trim() === '') {
            console.log("Empty input, nothing added");
            return knowledgebaseArray;  
        }
        const newArray = [...knowledgebaseArray, knowledgebaseInput.trim()];
        setKnowledgebaseArray(newArray);
        setKnowledgebaseInput('');
        return newArray;  
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
                /*
                if (node.name) {
                    node.name = node.name.replace('â†’', '→')
                                         .replace('âˆ¨', '∨')
                                         .replace('âˆ§', '∧')
                                         .replace('âŸº', '⟺')
                                         .replace('âŠ¥', '⊥');
                }
                */
                setScreen(1)
                return node;
            }
            if (node.child) {
                const result = findNodeById(node.child, id);
                console.log("this is the result.id", result)
                if (result) {
                    /*
                    if (result.name) {
                        result.name = result.name.replace('â†’', '→')
                                                 .replace('âˆ¨', '∨')
                                                 .replace('âˆ§', '∧')
                                                 .replace('âŸº', '⟺')
                                                 .replace('âŠ¥', '⊥');
                    }
                    */
                setScreen(1)
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

    {/*
    useEffect(() => {
        const firstChild = selectedNode?.child?.[0];
        if (
            selectedNode?.hasOneChild === "1" &&
            firstChild?.child?.length === 0 &&
            firstChild?.name !== "None"
        ) {
            setSelectedNodeId(firstChild.id);
        }
    }, [selectedNode]);

    
    useEffect(() => {
        if (selectedNode?.rule === "A" && screen === 0) {
            setScreen(1);
        }
    }, [selectedNode?.rule]);

    useEffect(() => {
        if (selectedNode?.rule === "A" && screen === 1) {
            setScreen(0);
        }
    }, [selectedNode?.rule]);
    */}



    const renderSelectedNodeAndChildren = () => {
        if (!selectedNode) return <p>Insira formula a provar</p>;

        return (
            <div className="tree-level">
                <NodeTreeRender
                    node={selectedNode}
                    renderTree={(nodes) => (
                        <div className="tree-level">
                            {nodes
                                .filter(node => node.name !== "None")
                                .map((node, index) => (
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
            knowledgebase: [setKnowledgebaseInput, knowledgebaseInputRef],
            auxiliar: [setAuxiliarInput, auxiliarInputRef]
        };

        const [setInput, inputRef] = inputMap[activeInput] || [];

        if (setInput && inputRef?.current) {
            const inputEl = inputRef.current;
            const start = inputEl.selectionStart;
            const end = inputEl.selectionEnd;

            const currentValue = inputEl.value;
            const newValue = currentValue.slice(0, start) + value + currentValue.slice(end);

            setInput(newValue);

            setTimeout(() => {
                inputEl.focus();
                const cursorPosition = start + value.length;
                inputEl.setSelectionRange(cursorPosition, cursorPosition);
            }, 0);
        }
    };



    return (
        <>
            <div className='main-container'>

                {!showTutorial && (
                    <>
                        <SegmentedControl
                            onChange={handleLanguageToggle}
                        />
                    
                        <ReactiveRnd
                            selectedNode={selectedNode}
                            language={language}
                            t={t}
                            knowledgebaseArray={knowledgebaseArray}
                            showRnd={showRnd}
                            screen={screen}
                        />
                    </>
                )}

                {screen === 0 ? (
                    <>

                    {!showTutorial && (
                        <>
                            <ActionButton
                                className='reset-bttn'
                                onClick={() => resetData("/api/reset")}
                                label={t("reset")}
                            />

                            <ActionButton 
                                className='save-bttn' 
                                onClick={() => saveData("/api/save")} 
                                label={t("download")} 
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

                            <button 
                                className="instructions-bttn"
                                onClick={() => setShowTutorial(prev => !prev)}
                            >
                                <FiAlertOctagon size={25} style={{ transform: 'rotate(180deg)' }} />
                            </button>

                            
                            {completedproof && (
                                <div className='proved-message-container'>
                                    <span>
                                        Prova Concluída
                                    </span>
                                </div>
                            )}
                    
                            
                            <div className="full-render-tree-container">
                                {renderTree(tree)}
                            </div>
                        </>
                    )}
                </>
                ) : screen === 1 ? (
                    <>

                       {!showTutorial && (
                            <>
                                <ActionButton
                                    className='reset-bttn'
                                    onClick={() => resetData("/api/reset")}
                                    label={t("reset")}
                                />

                                <ActionButton 
                                    className='save-bttn' 
                                    onClick={() => saveData("/api/save")} 
                                    label={t("download")} 
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

                                <button 
                                    className="instructions-bttn"
                                    onClick={() => setShowTutorial(prev => !prev)}
                                >
                                    <FiAlertOctagon size={25} style={{ transform: 'rotate(180deg)' }} />
                                </button>


                                <div className='operators-bttn'>
                                    {SYMBOLS.map(({ symbol, label}) => (
                                        <button
                                            key={symbol}
                                            aria-label={`Insert ${label} symbol to input`}
                                            onClick={() => appendToActiveInput(symbol)}
                                        >
                                            {symbol}
                                        </button>
                                    ))}
                                </div>

                                <div className={`knowledgebase-container ${isHidden ? 'off' : 'on'}`}>
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
                        
                
                                <div className={`expression-container ${isHidden ? 'off' : 'on'}`}>
                                    <input
                                        ref={expressionInputRef}
                                        type="text"
                                        value={expressionInput}
                                        onChange={(e) => setExpressionInput(e.target.value)}
                                        onFocus={() => setActiveInput('expression')}
                                        placeholder={t("expressionPlaceholder")}
                                        className='expression-input'
                                    />
                                    <button 
                                        className='add-expression-bttn' 
                                        aria-label='Start prove'
                                        onClick={() => {
                                            const updatedArray = addToArray(); // get updated kb array
                                            fetchData("/api/node", updatedArray);
                                        }}
                                    >
                                        <FiCheck size={20} />
                                    </button>
                                </div>

                                <div className={`rule-container ${isHidden ? 'on' : 'off'}`}>
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
                                            {Object.entries(ruleOptions).map(([key, rule]) => (
                                                <option key={key} value={key}>
                                                    {rule.label[language]}
                                                </option>
                                            ))}
                                        </select>
                                    </label>

                                    <button 
                                        className='add-rule-bttn' 
                                        aria-label='Apply rule'
                                        onClick={() => fetchData("/api/rules")}
                                    >
                                        <FiCheck size={20} />
                                    </button>

                            
                            
                                    {ruleOptions[ruleInput]?.needsAuxiliary && (
                                            <input
                                                ref={auxiliarInputRef}
                                                type="text"
                                                value={auxiliarInput}
                                                onChange={(e) => setAuxiliarInput(e.target.value)}
                                                onFocus={() => setActiveInput('auxiliar')}
                                                placeholder={
                                                    ruleOptions[ruleInput]?.auxFormulaPlaceholder?.[language]
                                                }
                                                className="auxiliar-formula-input"
                                            />
                                    )}

                                </div>


                                <div className="render-tree-container">
                                    {renderSelectedNodeAndChildren()}
                                </div>

                            </>
                        )}
                    </>
                ) : (
                    <>
                        {!showTutorial && (
                            <Info t={t}/>
                        )}
                    </>
                )}
            </div>

            {warning && (
                <Warning
                    message={warning}
                    onClose={() => setWarning('')}
                    autoDismiss={true}
                    duration={10000}
                />
            )}


           {showTutorial && (
                <div className="tutorial-overlay">
                    <div className="tutorial-content">

                        <h2>Instruções</h2>
                                
                        <p>This is the small tree view.</p>
                
                        <h3>Funcionalidades</h3>

                        <SegmentedControl
                            onChange={handleLanguageToggle}
                        />

                        <p style={{color:'blue'}}>Reniciar:</p>
                        <p>Serve para reniciar o programa</p>
                                
                        <p style={{color:'blue'}}>Baixar:</p> 
                        <p>Serve para baixar o programa</p>
                                
                        <p style={{color:'blue'}}>Abrir Upload:</p>
                        <p>Serve para carregar o programa</p>
                                
                        <p style={{ color: 'blue' }}>Conetivos proposicionais:</p>
                        <div>
                            {SYMBOLS.map(({ symbol, label }, index) => (
                                <span key={index} style={{ fontWeight:'bold',marginRight: '50px' }}>
                                    {symbol}
                                </span>
                            ))}
                        </div>

                        <p style={{ color: 'blue' }}>Hipóteses e Expressão:</p>
                        <p>Permitido letras minusculas e maisculas (Variaveis proposicionais)</p>
                        <p>
                            Exemplos:{" "}
                            <span style={{ fontWeight: "bold" }}>P1</span>,{" "}
                            <span style={{ fontWeight: "bold" }}>a95</span>,{" "}
                            <span style={{ fontWeight: "bold" }}>T</span>,{" "}
                            <span style={{ fontWeight: "bold" }}>b</span>
                        </p>

                        <p style={{ color: 'blue'}}>Node Colors</p>
                        <div 
                            style={{
                                display: 'flex',
                                gap: '10px',
                                justifyContent: 'center',
                                marginBottom: '30px'
                            }}
                        >   
                            <button
                                style={{
                                    padding: '8px 12px',
                                    backgroundColor: '#32de2f71',
                                    border: '1px solid #000000',
                                    borderRadius: '8px',
                                    fontSize: '14px',
                                    marginBottom: '-10px',
                                    textAlign: 'center',
                                    color: 'white',
                                    cursor: 'pointer',
                                }}
                            >
                                Problema Finalizado
                            </button>

                            <button
                                style={{
                                    padding: '8px 12px',
                                    backgroundColor: '#7dc5dd',
                                    border: '1px solid #000000',
                                    borderRadius: '8px',
                                    fontSize: '14px',
                                    marginBottom: '-10px',
                                    textAlign: 'center',
                                    color: 'white',
                                    cursor: 'pointer',
                                }}
                            >
                                Problema Intermédio
                            </button>

                            <button
                                style={{
                                    padding: '8px 12px',
                                    backgroundColor: '#e15d6a',
                                    border: '1px solid #000000',
                                    borderRadius: '8px',
                                    fontSize: '14px',
                                    marginBottom: '-10px',
                                    textAlign: 'center',
                                    color: 'white',
                                    cursor: 'pointer',
                                }}
                            >
                                Problema em Aberto
                            </button>
                        </div>
                        
                        <button onClick={() => setShowTutorial(false)}>Close ✕</button>

                    </div>

                </div>
            )}


        {!showTutorial && (
                <div className={`change-screen ${screen === 0 || screen === 1 ? 'on' : 'off'}`}>
                    <button 
                        className='full-tree-screen-bttn' 
                        aria-label='Switch to full tree view'
                        onClick={() => 
                            setScreen(0)
                        } 
                    />
                    <button 
                        className='small-tree-screen-bttn' 
                        aria-label='Switch to small tree view'
                        onClick={() => 
                            setScreen(1)
                        } 
                        />
                    <button 
                        className='help-screen-bttn' 
                        aria-label='Open help screen'
                        onClick={() => 
                            setScreen(2)
                        } 
                    />
                </div>
        )}
        </>
    );
}

export default PropositionLogicBody;