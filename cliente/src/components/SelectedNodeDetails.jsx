const SelectedNodeDetails = ({ node, language, translations, fallbackArray }) => {
    if (!node) return null;

    const { uuid, id, name, parentId, knowledge_base = fallbackArray } = node;
    const nodeKnowledgeBase = Object.entries(knowledge_base);
    const t = translations

    return (
        <div className="node-details">
            <p><strong>UUID:</strong>{uuid}</p>
            <p><strong>ID:</strong>{id}</p>
            <p><strong>{t("name")}:</strong><br />{name}</p>
            <p><strong>{t("parentId")}:</strong>{parentId}</p>
            <p><strong>{t("kb")}:</strong></p>
            <ul className="knowledge-list">
                {nodeKnowledgeBase.map(([key, value], index) => (
                    <li key={index}><strong style={{ color: 'red' }}>{key}:</strong> {value}</li>
                ))}
            </ul>
        </div>
    );
};


export default SelectedNodeDetails;