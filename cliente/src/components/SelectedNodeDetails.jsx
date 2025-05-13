const SelectedNodeDetails = ({ node, language, translations, fallbackArray }) => {
    if (!node) return null;

    const { uuid, id, name, parentId, knowledge_base, lambda = fallbackArray } = node;
    const nodeKnowledgeBase = Object.entries(knowledge_base);
    const t = translations

    return (
        <div className="node-details">
            <p><strong>{t("name")}:</strong><br />{name}</p>
            <p><strong>{t("kb")}:</strong></p>
            <ul className="knowledge-list">
                {nodeKnowledgeBase.map(([key, value], index) => (
                    <li key={index}><strong style={{ color: 'red' }}>{key}:</strong> {value}</li>
                ))}
            </ul>
            {/* se a lista for vazia escrver lista vazia*/}
        </div>
    );
};


export default SelectedNodeDetails;